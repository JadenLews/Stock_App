from .models import *
from .forms import *
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm 
import yfinance as yf
from .models import Watchlist, Stock
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
import pytz
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'pages/register.html', context)


@login_required
def home(request):
    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern).strftime("%I:%M:%S %p")
    current_date = datetime.now(eastern).strftime("%m/%d/%Y")
    
    portfolio_stocks = Portfolio.objects.filter(user=request.user)

    portfolio_data = []
    for entry in portfolio_stocks:
        stock_symbol = entry.stock.symbol
        quantity = entry.num_shares
        
        # Check if the stock data is cached
        stock_data = cache.get(f"stock_data_{stock_symbol}")
        if not stock_data:
            stock_info = yf.Ticker(stock_symbol)
            current_price = round(stock_info.history(period="1d")['Close'].iloc[0], 2)
            prev_close = stock_info.info['previousClose']
            percent_change = round(((current_price - prev_close) / prev_close) * 100, 2)
            price_change_direction = 'up' if percent_change > 0 else 'down'
            
            # Store the fetched data in cache for 5 minutes
            stock_data = {
                'current_price': current_price,
                'percent_change': percent_change,
                'change_direction': price_change_direction
            }
            cache.set(f"stock_data_{stock_symbol}", stock_data, timeout=300)
        
        portfolio_data.append({
            'symbol': stock_symbol,
            'company_name': entry.stock.company_name,
            'current_price': stock_data['current_price'],
            'percent_change': stock_data['percent_change'],
            'change_direction': stock_data['change_direction'],
            'stock_quantity': quantity,
        })

    notifications = Notification.objects.filter(user=request.user, status='unviewed').order_by('-created_at')
    paginator = Paginator(notifications, 5)  # Show only 5 notifications per page
    page = request.GET.get('page')
    notifications_paginated = paginator.get_page(page)

    watchlist_data = get_watchlist(request)

    context = {
        'markets': portfolio_data,
        'time': current_time,
        'date': current_date,
        'notifications': notifications_paginated,
        'notif_count': notifications.count(),
        'top_notif': notifications_paginated,
        'watchlist': watchlist_data
    }
    

    return render(request, "pages/home.html", context)


@login_required
def notifications(request, notification_id=None):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination for notifications
    paginator = Paginator(user_notifications, 5)  # Limit notifications to 5 per page
    page = request.GET.get('page')
    notifications_paginated = paginator.get_page(page)

    if notification_id:
        selected_notification = Notification.objects.get(id=notification_id, user=request.user)
        if selected_notification.status == 'unviewed':
            selected_notification.status = 'viewed'
            selected_notification.save()

        detailed_notifications = Notification.objects.filter(
            user=request.user,
            stock__symbol__iexact=selected_notification.stock.symbol
        ).order_by('-created_at')
        selected_notification_id = notification_id
    else:
        detailed_notifications = None
        selected_notification_id = None

    watchlist_data = get_watchlist(request)

    context = {
        'notifications': notifications_paginated,
        'detailed_notifications': detailed_notifications,
        'selected_notification_id': selected_notification_id,
        'watchlist': watchlist_data
    }

    return render(request, "pages/notifications.html", context)


@login_required
def portfolio(request):
    user_watchlist = Watchlist.objects.filter(user=request.user)
    stock_data = []

    for entry in user_watchlist:
        stock_symbol = entry.stock.symbol
        stock_info = yf.Ticker(stock_symbol)
        
        current_price = round(stock_info.history(period="1d")['Close'].iloc[0], 2)
        prev_close = stock_info.info['previousClose']
        percent_change = round(((current_price - prev_close) / prev_close) * 100, 2)
        price_change_direction = 'up' if percent_change > 0 else 'down'

        stock_data.append({
            'symbol': stock_symbol,
            'company_name': entry.stock.company_name,
            'current_price': current_price,
            'percent_change': percent_change,
            'change_direction': price_change_direction
        })
    
    portfolio_stocks = Portfolio.objects.filter(user=request.user)
    portfolio_data = []
    sector_count = {}
    

    for entry in portfolio_stocks:
        stock_symbol = entry.stock.symbol
        stock_quantity = entry.num_shares
        stock_info = yf.Ticker(stock_symbol)
        sector = stock_info.info.get('sector', 'N/A')
        
        current_price = round(stock_info.history(period="1d")['Close'].iloc[0], 2)
        prev_close = stock_info.info['previousClose']
        percent_change = round(((current_price - prev_close) / prev_close) * 100, 2)
        price_change_direction = 'up' if percent_change > 0 else 'down'
        
        if percent_change < -4:
            stock_notifs = Notification.objects.filter(stock=entry.stock)
            notif_count = 0

            # Get the current UTC time
            current_time = timezone.now()
            print(entry.stock.symbol)

            for notif in stock_notifs:
                # Check if created_at and current_time are on the same date
                if notif.created_at.date() == current_time.date():
                    notif_count += 1
                    
            if notif_count == 0:
                Notification.objects.create(
                message=f"Stock has fallen very low to {percent_change}%", 
                user=request.user, 
                stock=entry.stock,
                status='unviewed', 
                created_at=current_time
            )
                
        if percent_change > 4:
            stock_notifs = Notification.objects.filter(stock=entry.stock)
            notif_count = 0

            # Get the current UTC time
            current_time = timezone.now()
            print(entry.stock.symbol)

            for notif in stock_notifs:
                # Check if created_at and current_time are on the same date
                if notif.created_at.date() == current_time.date():
                    notif_count += 1
                    
            if notif_count == 0:
                Notification.objects.create(
                message=f"Stock has risen very high to {percent_change}%", 
                user=request.user, 
                stock=entry.stock,
                status='unviewed', 
                created_at=current_time
            )
        
        if sector in sector_count:
            sector_count[sector] += 1 * int(stock_quantity)
        else:
            sector_count[sector] = 1 * int(stock_quantity)
        

        portfolio_data.append({
            'symbol': stock_symbol,
            'company_name': entry.stock.company_name,
            'quantity': stock_quantity,
            'sector': sector,
            'current_price': current_price,
            'percent_change': percent_change,
            'change_direction': price_change_direction,
            'total_value': float(stock_quantity) * float(current_price),
            'value_lost': (float(percent_change) / 100) * (float(stock_quantity) * float(current_price))
        })

    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern).strftime("%I:%M:%S %p")
    current_date = datetime.now(eastern).strftime("%m/%d/%Y")

    context = {
        'watchlist': stock_data,
        'markets': portfolio_data,
        'time': current_time,
        'date': current_date,
        'sector_count': sector_count
    }
    
    return render(request, "pages/portfolio.html", context)


def stock_details(request, symbol, time_frame='1mo'):
    # Initialize the stock object using yfinance
    stock = yf.Ticker(symbol)
    
    # Set the interval based on the selected time frame
    interval = "1d"
    if time_frame == "1d":
        interval = "15m"
    elif time_frame == "5d":
        interval = "30m"
    
    # Check if the stock data is cached
    stock_data_cache_key = f"stock_data_{symbol}_{time_frame}"
    stock_info = cache.get(stock_data_cache_key)
    print(stock_info)
    
    if stock_info is None or stock_info.empty:
        print("You Made It Here!")
        # Fetch the stock data if it's not cached or if the cached data is empty
        stock_info = stock.history(period=time_frame, interval=interval)
        
        # Handle case when stock_info is empty (e.g., no data for the requested period)
        if stock_info.empty:
            return render(request, 'pages/stock_details.html', {'error': 'No data available for this time period.'})
        
        # Cache the stock data for 10 minutes
        cache.set(stock_data_cache_key, stock_info, timeout=600)  # Cache for 10 minutes
    
    # Extract dates and closing prices from the stock_info DataFrame
    dates = stock_info.index.strftime("%Y-%m-%d %H:%M").tolist() if interval != "1d" else stock_info.index.strftime("%Y-%m-%d").tolist()
    closing_prices = stock_info['Close'].tolist()

    # Get the company name and other stock information from yfinance
    company_name = stock.info.get('shortName', 'N/A')

    # Get or create the Stock record in your database
    stock_item, created = Stock.objects.get_or_create(
        symbol=symbol,
        defaults={
            'company_name': company_name,
            'sector': stock.info.get("sector", "N/A"),
            'price': round(stock_info['Close'].iloc[-1], 2) if not stock_info.empty else None
        }
    )

    watchlist_data = get_watchlist(request)

    # Prepare context data to pass to the template
    context = {
        'stock': {
            'symbol': symbol,
            'company_name': company_name,
            'price': round(stock_info['Close'].iloc[-1], 2) if not stock_info.empty else None,
        },
        'symbol': symbol,
        'time_frame': time_frame,
        'dates': json.dumps(dates),
        'closing_prices': json.dumps(closing_prices),
        'watchlist': watchlist_data
    }

    # Return the rendered response
    return render(request, 'pages/stock_details.html', context)


def user_watchlist(request):
    user_watchlist = Watchlist.objects.filter(user=request.user)
    stock_data = []

    for entry in user_watchlist:
        stock_symbol = entry.stock.symbol
        stock_info = yf.Ticker(stock_symbol)
        
        current_price = round(stock_info.history(period="1d")['Close'].iloc[0], 2)
        prev_close = stock_info.info['previousClose']
        percent_change = round(((current_price - prev_close) / prev_close) * 100, 2)
        price_change_direction = 'up' if percent_change > 0 else 'down'

        stock_data.append({
            'symbol': stock_symbol,
            'company_name': entry.stock.company_name,
            'current_price': current_price,
            'percent_change': percent_change,
            'change_direction': price_change_direction
        })
    
    context = {
        'watchlist': stock_data
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
    
@login_required
def add_watchlist(request):
    if request.method == 'POST':
        stock_symbol = request.POST.get('stock_symbol')

        try:
            # Fetch the stock object
            stock = Stock.objects.get(symbol=stock_symbol)

            # Check if a Watchlist entry already exists for the user and the stock
            if not Watchlist.objects.filter(user=request.user, stock=stock).exists():
                # If it doesn't exist, create the watchlist item
                Watchlist.objects.create(
                    user=request.user,
                    stock=stock,
                )
                messages.success(request, f'Added {stock_symbol} to your watchlist.')
            else:
                # If it already exists, do nothing
                messages.info(request, f'{stock_symbol} is already in your watchlist.')

        except Stock.DoesNotExist:
            messages.error(request, 'Stock not found.')
        except Exception as e:
            messages.error(request, f'Error executing trade: {e}')
        
        # Redirect back to the stock details page or wherever you want
        return redirect('stock_details', symbol=stock_symbol)

def get_watchlist(request):
    user_watchlist = Watchlist.objects.filter(user=request.user)
    stock_data = []

    for entry in user_watchlist:
        stock_symbol = entry.stock.symbol
        stock_info = yf.Ticker(stock_symbol)
        
        current_price = round(stock_info.history(period="1d")['Close'].iloc[0], 2)
        prev_close = stock_info.info['previousClose']
        percent_change = round(((current_price - prev_close) / prev_close) * 100, 2)
        price_change_direction = 'up' if percent_change > 0 else 'down'

        stock_data.append({
            'symbol': stock_symbol,
            'company_name': entry.stock.company_name,
            'current_price': current_price,
            'percent_change': percent_change,
            'change_direction': price_change_direction
        })
    
    return stock_data