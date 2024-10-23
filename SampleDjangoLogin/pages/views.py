from .models import *
from .forms import *
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm 
import yfinance as yf
from .models import Stock
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Watchlist, Stock
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # form.save() will automatically hash the password and save the user.
            form.save()
            messages.success(request, 'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'pages/register.html', context)



def home(request):
    return render(request, "pages/home.html")

def watchlist(request):
    return render(request, "pages/watchlist.html")

def notifications(request):
    return render(request, "pages/notifications.html")

def portfolio(request):
    return render(request, "pages/portfolio.html")

def stock_details(request, symbol):
    try:
        # Use yfinance to get stock info
        stock_info = yf.Ticker(symbol)
        stock_price = stock_info.history(period="1d")['Close'].iloc[0] # Fetch current price
        
        # Try to get the stock if it exists, or create a new entry
        stock, created = Stock.objects.get_or_create(
            symbol=symbol,
            defaults={
                'company_name': stock_info.info['longName'],
                'sector': stock_info.info.get('sector', 'N/A'),
                'price': stock_price
            }
        )
        
        if not created:
            # Update the price if the stock already exists
            stock.price = stock_price
            stock.save()

        return render(request, 'pages/stock_details.html', {'stock': stock})

    except KeyError:
        return render(request, 'pages/stock_details.html', {'error': 'Invalid stock symbol or missing data from the API.'})
    except IntegrityError:
        return render(request, 'pages/stock_details.html', {'error': 'Error saving the stock.'})
    except IndexError:
        return render(request, 'pages/stock_details.html', {'error': 'Invalid stock symbol or missing data from the API.'})


@login_required
def user_watchlist(request):
    # Fetch the watchlist for the current logged-in user
    user_watchlist = Watchlist.objects.filter(user=request.user)

    # Initialize an empty list to hold stock data
    stock_data = []

    # Loop through the user's watchlist and fetch stock data from Yahoo Finance
    for entry in user_watchlist:
        stock_symbol = entry.stock.symbol  # Get the stock symbol from your model
        stock_info = yf.Ticker(stock_symbol)  # Fetch data for the stock using Yahoo Finance
        
        # Fetch current stock price and previous close price
        current_price = round(stock_info.history(period="1d")['Close'].iloc[0], 2)  # Round to 2 decimals
        prev_close = stock_info.info['previousClose']

        # Calculate percentage change
        percent_change = round(((current_price - prev_close) / prev_close) * 100, 2)

        # Determine if the stock is up or down based on the percentage change
        price_change_direction = 'up' if percent_change > 0 else 'down'

        # Append the data for this stock to the stock_data list
        stock_data.append({
            'symbol': stock_symbol,
            'company_name': entry.stock.company_name,
            'current_price': current_price,
            'percent_change': percent_change,
            'change_direction': price_change_direction
        })

    # Pass the stock data to the template
    context = {
        'watchlist': stock_data,
    }
    
    return render(request, 'pages/watchlist.html', context)
@login_required
@require_POST
def toggle_watchlist(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    user = request.user

    if request.method == 'POST':
        action = json.loads(request.body).get('action')
        print(action)
        if action == 'add':
            Watchlist.objects.get_or_create(stock=stock, user=user)
        elif action == 'remove':
            Watchlist.objects.filter(stock=stock, user=user).delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

@login_required
def execute_trade(request):
    if request.method == 'POST':
        stock_symbol = request.POST.get('stock_symbol')
        trade_action = request.POST.get('trade_action')  # Get the action (buy/sell)
        quantity = request.POST.get('quantity')

        try:
            # Fetch the stock object
            stock = Stock.objects.get(symbol=stock_symbol)
            
            # Convert quantity to a decimal
            quantity = Decimal(quantity)
            
            # Get the user's portfolio (or create if it doesn't exist)
            portfolio_item, created = Portfolio.objects.get_or_create(
                user=request.user,
                stock=stock,
                defaults={'num_shares': Decimal('0')}  # Default to 0 shares
            )
            
            if trade_action == 'buy':
                portfolio_item.num_shares += quantity  # Add shares if buying
            elif trade_action == 'sell':
                portfolio_item.num_shares -= quantity  # Subtract shares if selling
                if portfolio_item.num_shares < 0:
                    messages.error(request, "You can't sell more shares than you own!")
                    return redirect('stock_details', symbol=stock_symbol)
            
            # If all good, save the portfolio item
            portfolio_item.save()

            messages.success(request, f'Trade executed: {trade_action.capitalize()} {quantity} shares of {stock_symbol}')
        except Stock.DoesNotExist:
            messages.error(request, 'Stock not found.')
        except Exception as e:
            messages.error(request, f'Error executing trade: {e}')
        
        # Redirect back to the stock details page or wherever you want
        return redirect('stock_details', symbol=stock_symbol)