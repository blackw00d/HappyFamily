from django.utils.safestring import mark_safe
from HappyFamily.settings import EMAIL_HOST_USER, TELEGRAM_TOKEN, TELEGRAM_ADMIN
from .models import Items, Images, Orders, OrderItem, CityPrice, City
from django.core.mail import send_mail
from django.db.models import F
from .telegram_api import Telegram


def send_email(email, created, pay_method):
    """ Отправка письма о создании заказа """
    if pay_method == 'online':
        pay = "Для оплаты нажмите на кнопку " \
              "</td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "height =\"25\" align=\"left\" valign=\"top\"></td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" height=\"50\">" \
              "<table " \
              "width =\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" width=\"126\"></td>" \
              "<td " \
              "align =\"center\" valign=\"middle\" height=\"50\" width=\"248\" bgcolor=\"#0082b2\" " \
              "style=\"font-size:14px;line-height:19px;color:#ffffff;font-family:Arial, Helvetica, " \
              f"sans-serif;\"><a href=\"https://hf86.ru/enter/?forget={email}\" target=\"_blank\" " \
              "style=\"color:#ffffff;text-decoration:none;\"><span " \
              "style=\"font-size:14px;line-height:19px;color:#ffffff;font-family:Arial, Helvetica, " \
              "sans-serif;\">Оплатить</span></a></td>" \
              "<td " \
              "align =\"left\" valign=\"top\" width=\"126\"></td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "</td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "height =\"25\" align=\"left\" valign=\"top\"></td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font-family" \
              ":Arial, Helvetica, sans-serif;\">Или скопируйте данную строку в браузер:<br>" \
              "<a " \
              f"href =\"https://hf86.ru/enter/?forget={email}\" target=\"_blank\" " \
              "style=\"text-decoration: none;color:#0082b2;\"><span " \
              f"style=\"color:#0082b2;\">https://hf86.ru/enter/?forget={email}</span></a>" \
              "</td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "height =\"30\" align=\"left\" valign=\"top\"></td>" \
              "</tr>"
    else:
        pay = "Наш менеджер свяжется с Вами в ближайшее время.<br><br>Для отслеживания заказа \
              зарегистрируйтесь на сайте.<br>" \
              "</td>" \
              "</tr>"
    message = "<!DOCTYPE " \
              "html>" \
              "<html " \
              "lang=\"en\">" \
              "<head>" \
              "<link rel=\"icon\" href=\"https://hf86.ru/img/logo.ico\">" \
              "<meta charset=\"UTF-8\">" \
              "<title>Happy " \
              "Family " \
              "Surgut </title>" \
              "<link rel =\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.3.1/css/all.css\" " \
              "integrity=\"sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU\" " \
              "crossorigin=\"anonymous\">" \
              "</head>" \
              "<body>" \
              "<table " \
              "width =\"100%ds\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"center\" valign=\"top\">" \
              "<table " \
              "width =\"640\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"center\" valign=\"top\" width=\"600\">" \
              "<table " \
              "width =\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" height=\"15\"></td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\">" \
              "<table " \
              "width =\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" width=\"95\" height=\"36\"><a href=\"https://hf86.ru\" " \
              "target=\"_blank\"><img src=\"https://hf86.ru/img/logo.png\" width=\"95\" " \
              "style=\"display:block;\" " \
              "border=\"0\" alt=\"Happy Family\"></a>" \
              "</td>" \
              "<td " \
              "align =\"right\" valign=\"middle\" style=\"font-family:Arial, Helvetica, " \
              "sans-serif;font-size:12px;line-height:15px;color:#585858;\">" \
              "HAPPY FAMILY SURGUT" \
              "</td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "</td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" height=\"25\">" \
              "</td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" style=\"border:1px solid #dddddd;\" bgcolor=\"#ffffff\">" \
              "<table " \
              "width =\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" width=\"49\">" \
              "</td>" \
              "<td " \
              "align =\"left\" valign=\"top\" width=\"500\">" \
              "<table " \
              "width =\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" height=\"50\"></td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              " align =\"left\" valign=\"top\" style=\"font-size:22px;line-height:28px;color:#333333;font-weight" \
              f":bold;font-family:Arial, Helvetica, sans-serif;\">Здравствуйте,</td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "height =\"20\" align=\"left\" valign=\"top\"></td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font-family" \
              ":Arial, Helvetica, sans-serif;\">" \
              f"Вы сделали <strong>{created}</strong> на сайте " \
              "<a href =\"https://hf86.ru\" target=\"_blank\" style=\"text-decoration:none;color:#585858;\"><span " \
              "style=\"text-decoration:none;color:#585858;\">hf86.ru</span></a>." \
              "<br><br>" \
              f"{pay}" \
              "<tr>" \
              "<td " \
              "height =\"30\" align=\"left\" valign=\"top\" style=\"border-top:1px solid #dddddd;\"></td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font-family" \
              ":Arial, Helvetica, sans-serif;\">Спасибо, что Вы выбрали <a href=\"https://hf86.ru\" " \
              "target=\"_blank\" style=\"text-decoration:none;color:#585858;\"><span " \
              "style=\"text-decoration:none;color:#585858;\">hf86.ru</span></a>. Удачи!<br><br>" \
              "<strong> С уважением, команда Happy Family </strong>" \
              "</td>" \
              "</tr>" \
              "<tr>" \
              "<td align =\"left\" valign=\"top\" height=\"50\"></td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "</td>" \
              "<td align =\"left\" valign=\"top\" width=\"49\"></td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "</td>" \
              "</tr>" \
              "<tr>" \
              "<td align =\"left\" valign=\"top\" height=\"40\"></td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "</td>" \
              "<td align =\"center\" valign=\"top\" width=\"20\"></td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "<table width =\"640\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"center\" valign=\"top\" width=\"20\"></td>" \
              "<td " \
              "align =\"center\" valign=\"top\" width=\"600\">" \
              "<table " \
              "width =\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"center\" valign=\"top\"><a href=\"https://hf86.ru\" target=\"_blank\"><img " \
              "src=\"https://hf86.ru/img/logo.png\" width=\"95\" border=\"0\" alt=\"Logo\"></a></td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"center\" valign=\"top\" \
              style=\"font-size:14px;line-height:19px;color:#585858;font-family:Arial, Helvetica, sans-serif;\">" \
              "Happy Family Surgut " \
              "</td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" height=\"20\"></td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"center\" valign=\"top\">" \
              "<table " \
              "<table " \
              "width =\"100%\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\">" \
              "<tbody>" \
              "<tr>" \
              "<td " \
              "align =\"center\" valign=\"top\" width=\"120\"></td>" \
              "<td " \
              "align =\"center\" valign=\"top\" width=\"30\">" \
              "<a" \
              "href =\"https://instagram.com/happyfamily_hmao\" title=\"Instagram\" style=\"color:blue\">" \
              "<img " \
              "src =\"https://hf86.ru/img/icons/instagram.png\" height=\"20\">" \
              "</a>" \
              "</td>" \
              "<td " \
              "align =\"center\" valign=\"top\" width=\"30\">" \
              "<a " \
              "href =\"https://vk.com/happyfamily_hmao\" title=\"VK\" style=\"color:blue\">" \
              "<img " \
              "src =\"https://hf86.ru/img/icons/vk.png\" height=\"20\">" \
              "</a>" \
              "</td>" \
              "<td " \
              "align =\"center\" valign=\"top\" width=\"120\"></td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "</td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"left\" valign=\"top\" height=\"30\"></td>" \
              "</tr>" \
              "<tr>" \
              "<td " \
              "align =\"center\" valign=\"top\" \
              style=\"font-size:11px;line-height:16px;color:#585858;font-family:Arial, Helvetica, sans-serif;\">" \
              "Copyright © 2020" \
              "</td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "</td>" \
              "<td " \
              "align =\"center\" valign=\"top\" width=\"20\"></td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "</td>" \
              "</tr>" \
              "</tbody>" \
              "</table>" \
              "</body>" \
              "</html>"
    subject_text = f"{created} на сайте Happy Family"

    send_mail(subject=subject_text, from_email=EMAIL_HOST_USER, recipient_list=[email],
              html_message=message, message=message)
    return True


def get_all_items(city):
    """ Получение списка товаров """
    return CityPrice.objects.filter(city__name=city, count__gt=0).order_by('id')


def get_all_cities():
    """ Получение списка городов """
    return City.objects.all().order_by('id')


def get_item_image(item_name):
    """ Получение изображения товара """
    item = Items.objects.filter(name=item_name).values('id')[0]['id']
    image_url = Images.objects.filter(name_id=item).values('image').first()['image']
    return image_url


def add_item_to_basket(basket, name, price, image_url):
    """ Добавление товара в корзину """
    append = basket.get(name, None)
    basket.update({name: {'price': price, 'img': image_url}})

    if not append:
        data = mark_safe(f"<div class=\"product\"><div class=\"product-image\"><img src=\"media/{image_url}\"></div"
                         f"><div class=\"product-details\"><div class=\"product-title\">{name}</div></div><div "
                         f"class=\"product-price\">{price} &#x20BD;</div><div class=\"product-removal\"><a "
                         f"href=\"#\" class=\"remove-product\" data-name=\"{name}\"><i class=\"fas "
                         "fa-trash-alt\"></i></a></div></div>")
    else:
        data = ''

    return data


def get_basket_with_len(basket, city):
    """ Полученеи корзины и количества товаров в ней """
    for item in basket:
        exists = CityPrice.objects.filter(item__name=item, city__name=city, count__gt=0).exists()
        price = CityPrice.objects.filter(item__name=item, city__name=city)[0].get_sale_price()
        if exists:
            basket[item] = {'price': price, 'img': get_item_image(item), 'sold': False}
        else:
            basket[item] = {'price': price, 'img': get_item_image(item), 'sold': True}
    basket_len = len(basket.values())
    return {'basket': basket, 'basket_len': basket_len}


def create_order(phone, email, pay, city):
    """ Внесение заказа в базу данных """
    return Orders.objects.create(phone=phone, email=email, pay=pay, city=city)


def add_items_to_order(basket, created, city):
    """ Внесение товаров в заказ и уменьшение количества товаров на складе города покупки"""
    for item in basket:
        exists = CityPrice.objects.filter(item__name=item, city__name=city, count__gt=0).exists()
        price = CityPrice.objects.filter(item__name=item, city__name=city)[0].get_sale_price()
        if exists:
            item_name = CityPrice.objects.get(item__name=item)
            OrderItem.objects.create(order=created, items=item_name, order_price=price)
            CityPrice.objects.filter(city__name=city, item__name=item).values('count', 'reserved').update(
                count=F('count') - 1, reserved=F('reserved') + 1)
    basket.clear()


def telegram_add_call(phone):
    """ Отправка сообщения в группу Telegram от формы обратной связи """
    telegram = Telegram(TELEGRAM_TOKEN)
    telegram.send_message_to_user(TELEGRAM_ADMIN, f'Клиент с номером {phone} заказал обратный звонок')


def telegram_make_order(phone, order, city):
    """ Отправка сообщения в группу Telegram о совершении заказа """
    telegram = Telegram(TELEGRAM_TOKEN)
    telegram.send_message_to_user(TELEGRAM_ADMIN, f'Клиент с номером {phone} сделал {order} в г.{city}')
