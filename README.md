Приложение развернуто на хостинге PythonAnywhere https://maxsar.pythonanywhere.com/
https://maxsar.pythonanywhere.com/item/1 для просмотра первого товара, его можно оплатить сразу, нажав на кнопку buy или добавить в заказ 
одну единицу товара кнопкой add to order или удалить одну единицу товара из заказа кнопкой remove from order
получить checkout_session.id для товара https://maxsar.pythonanywhere.com/buy/<pk>/ для заказа https://maxsar.pythonanywhere.com/buy-order/
по ссылке https://maxsar.pythonanywhere.com/order/ можно получить информацию о заказе и оплатить, нажав на кнопку buy
расчет будет производится по валюте товара, при добавлении товаров с разной валютой оплата будет происходит в валюте, сумма которой больше с учетом курса
логин и пароль от административной панели admin admin
