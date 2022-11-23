import random

import stripe
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from .models import Item, Order
from django.views.generic import TemplateView
import requests
import json

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = Item.objects.get(id=item_id)
        domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': item.currency.lower(),
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "item_id": item.id
            },
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

    def post(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = Item.objects.get(id=item_id)
        domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': item.currency.lower(),
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "item_id": item.id
            },

            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',

        )
        return JsonResponse({
            'id': checkout_session.id
        })


class CreateCheckoutSessionOrderView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        orders = list(Order.objects.filter(user=user))
        domain = "http://127.0.0.1:8000"
        order_id = random.randint(10000000, 99999999)
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.request("GET", url).json()
        usd = response['Valute']['USD']['Value']
        eur = response['Valute']['EUR']['Value']
        quote = usd / eur
        total_eur = 0
        total_usd = 0
        for order in orders:
            if order.quantity == 0:
                orders.remove(order)
            if order.item.currency == 'USD':
                total_usd += order.item.price
            else:
                total_eur += order.item.price
        if total_usd * quote > total_eur:
            total_currency = 'USD'
        else:
            total_currency = 'EUR'
        line_items = []
        for order in orders:

            if order.item.currency == 'EUR' and total_currency == 'USD':
                unit_amount = order.item.price / quote
            elif order.item.currency == 'USD' and total_currency == 'EUR':
                unit_amount = order.item.price * quote
            else:
                unit_amount = order.item.price

            item = {
                'price_data': {
                    'currency': total_currency.lower(),
                    'unit_amount': int(unit_amount),
                    'product_data': {
                        'name': order.item.name
                    },
                },
                'quantity': order.quantity,
            }
            line_items.append(item)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            metadata={
                "order_id": order_id
            },
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

    def post(self, request, *args, **kwargs):
        user = self.request.user
        orders = list(Order.objects.filter(user=user))
        domain = "http://127.0.0.1:8000"
        order_id = random.randint(10000000, 99999999)
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.request("GET", url).json()
        usd = response['Valute']['USD']['Value']
        eur = response['Valute']['EUR']['Value']
        quote = usd / eur
        total_eur = 0
        total_usd = 0
        for order in orders:
            if order.quantity == 0:
                orders.remove(order)
            if order.item.currency == 'USD':
                total_usd += order.item.price
            else:
                total_eur += order.item.price
        if total_usd * quote > total_eur:
            total_currency = 'USD'
        else:
            total_currency = 'EUR'
        line_items = []
        for order in orders:

            if order.item.currency == 'EUR' and total_currency == 'USD':
                unit_amount = order.item.price / quote
            elif order.item.currency == 'USD' and total_currency == 'EUR':
                unit_amount = order.item.price * quote
            else:
                unit_amount = order.item.price

            item = {
                'price_data': {
                    'currency': total_currency.lower(),
                    'unit_amount': int(unit_amount),
                    'product_data': {
                        'name': order.item.name
                    },
                },
                'quantity': order.quantity,
            }
            line_items.append(item)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            metadata={
                "order_id": order_id
            },
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class ItemLandingPageView(TemplateView):
    template_name = "stripe_app/landing.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        item = Item.objects.get(pk=pk)
        context = super(ItemLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "item": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class OrderLandingPageView(TemplateView):
    template_name = "stripe_app/order.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        total_order_usd = 0
        total_order_euro = 0
        for order in orders:
            if order.item.currency == 'USD':
                order_price = order.item.price * order.quantity / 100
                total_order_usd += order_price
            else:
                order_price = order.item.price * order.quantity / 100
                total_order_euro += order_price

        context = super(OrderLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "orders": orders,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "total_order_usd": total_order_usd,
            "total_order_euro": total_order_euro,
        })
        return context


def add_to_order(request, item_id):
    item = Item.objects.get(id=item_id)
    orders = Order.objects.filter(user=request.user, item=item)

    if not orders.exists():
        Order.objects.create(user=request.user, item=item, quantity=1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        order = orders.first()
        order.quantity += 1
        order.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_order(request, item_id):
    item = Item.objects.get(id=item_id)
    orders = Order.objects.filter(user=request.user, item=item)

    if not orders.exists():
        Order.objects.create(user=request.user, item=item, quantity=1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        try:

            order = orders.first()
            order.quantity -= 1
            order.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except IntegrityError:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
