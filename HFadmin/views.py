from hashlib import md5
from django.db.models import F
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from HFhtml.models import Users
from django.contrib.auth import login, authenticate
from django.db.models.functions import Right, MD5
from django.core.mail import send_mail
from HappyFamily.settings import EMAIL_HOST_USER


def _send_email(user, email, subject):
    """ Отправка письма при регистрации, письма со ссылкой для смены пароля, письма об успешной смене пароля """
    message, subject_text = "", ""
    if subject == 'reset':
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
                  "HAPPY " \
                  "FAMILY " \
                  "SURGUT" \
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
                  f":bold;font-family:Arial, Helvetica, sans-serif;\">Привет {user[0]['email']},</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td " \
                  "height =\"20\" align=\"left\" valign=\"top\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td " \
                  "align =\"left\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font-family" \
                  ":Arial, Helvetica, sans-serif;\">" \
                  "Для " \
                  "смены " \
                  "пароля " \
                  "на " \
                  "сайте <a " \
                  "href =\"https://hf86.ru\" target=\"_blank\" style=\"text-decoration:none;color:#585858;\"><span " \
                  "style=\"text-decoration:none;color:#585858;\">hf86.ru</span></a>." \
                  "<br><br>" \
                  "Нажмите " \
                  "на " \
                  "кнопку " \
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
                  f"sans-serif;\"><a href=\"https://hf86.ru/enter/?forget={user[0]['reset']}\" target=\"_blank\" " \
                  "style=\"color:#ffffff;text-decoration:none;\"><span " \
                  "style=\"font-size:14px;line-height:19px;color:#ffffff;font-family:Arial, Helvetica, " \
                  "sans-serif;\">СМЕНИТЬ ПАРОЛЬ</span></a></td>" \
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
                  f"href =\"https://hf86.ru/enter/?forget={user[0]['reset']}\" target=\"_blank\" " \
                  "style=\"text-decoration: none;color:#0082b2;\"><span " \
                  f"style=\"color:#0082b2;\">https://hf86.ru/enter/?forget={user[0]['reset']}</span></a>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td " \
                  "height =\"30\" align=\"left\" valign=\"top\"></td>" \
                  "</tr>" \
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
                  "align =\"center\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font-family:Arial, Helvetica, sans-serif;\">" \
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
                  "align =\"center\" valign=\"top\" style=\"font-size:11px;line-height:16px;color:#585858;font-family:Arial, Helvetica, sans-serif;\">" \
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
        subject_text = "Смена пароля Happy Family"
    if subject == 'signup':
        message = "<!DOCTYPE html>" \
                  "<html lang=\"en\">" \
                  "<head>" \
                  "<link rel=\"icon\" href=\"https://hf86.ru/img/logo.ico\">" \
                  "<meta charset=\"UTF-8\">" \
                  "<title>Happy Family Surgut</title>" \
                  "<link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.3.1/css/all.css\" " \
                  "integrity=\"sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU\" " \
                  "crossorigin=\"anonymous\">" \
                  "</head>" \
                  "<body>" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\">" \
                  "<table width=\"640\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" width=\"600\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"15\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" width=\"95\" height=\"36\"><a href=\"https://hf86.ru\" " \
                  "target=\"_blank\"><img src=\"https://hf86.ru/img/logo.png\" width=\"95\" " \
                  "style=\"display:block;\" border=\"0\" alt=\"Happy Family\"></a>" \
                  "</td>" \
                  "<td align=\"right\" valign=\"middle\" style=\"font-family:Arial, Helvetica, " \
                  "sans-serif;font-size:12px;line-height:15px;color:#585858;\">" \
                  "HAPPY FAMILY SURGUT" \
                  "</td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"25\">" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" style=\"border:1px solid #dddddd;\" bgcolor=\"#ffffff\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  " <td align=\"left\" valign=\"top\" width=\"49\">" \
                  "</td>" \
                  "<td align=\"left\" valign=\"top\" width=\"500\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  " <tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"50\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" style=\"font-size:22px;line-height:28px;color:#333333;font" \
                  f"-weight:bold;font-family:Arial, Helvetica, sans-serif;\">Привет {email},</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td height=\"20\" align=\"left\" valign=\"top\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font" \
                  "-family:Arial, Helvetica, sans-serif;\">" \
                  "Мы рады видеть Вас частью <a href=\"https://hf86.ru\" target=\"_blank\" " \
                  "style=\"text-decoration:none;color:#585858;\"><span " \
                  "style=\"text-decoration:none;color:#585858;\">hf86.ru</span></a>." \
                  "<br><br>" \
                  "Для входа на сайт нажмите кнопку." \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td height=\"25\" align=\"left\" valign=\"top\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"50\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" width=\"126\"></td>" \
                  "<td align=\"center\" valign=\"middle\" height=\"50\" width=\"248\" bgcolor=\"#0082b2\" " \
                  "style=\"font-size:14px;line-height:19px;color:#ffffff;font-family:Arial, Helvetica, " \
                  "sans-serif;\"><a href=\"https://hf86.ru/enter/\" target=\"_blank\" " \
                  "style=\"color:#ffffff;text-decoration:none;\"><span " \
                  "style=\"font-size:14px;line-height:19px;color:#ffffff;font-family:Arial, Helvetica, " \
                  "sans-serif;\">ВОЙТИ</span></a></td>" \
                  "<td align=\"left\" valign=\"top\" width=\"126\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td height=\"30\" align=\"left\" valign=\"top\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td height=\"30\" align=\"left\" valign=\"top\" style=\"border-top:1px solid #dddddd;\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font" \
                  "-family:Arial, Helvetica, sans-serif;\">Спасибо, что Вы выбрали <a href=\"http://hf86.ru\" " \
                  "target=\"_blank\" style=\"text-decoration:none;color:#585858;\" rel=\" noopener " \
                  "noreferrer\"><span style=\"text-decoration:none;color:#585858;\">hf86.ru</span></a>. " \
                  "Удачи!<br><br>" \
                  "<strong>С уважением, команда Happy Family</strong>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"50\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "<td align=\"left\" valign=\"top\" width=\"49\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"40\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "<td align=\"center\" valign=\"top\" width=\"20\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "<table width=\"640\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" width=\"20\"></td>" \
                  "<td align=\"center\" valign=\"top\" width=\"600\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\"><a href=\"http://hf86.ru\" target=\"_blank\"><img " \
                  "src=\"https://hf86.ru/img/logo.png\" width=\"95\" border=\"0\" alt=\"Logo\"></a></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font" \
                  "-family:Arial, Helvetica, sans-serif;\">" \
                  "Happy Family Surgut" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"20\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\">" \
                  "<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" width=\"120\"></td>" \
                  "<td align=\"center\" valign=\"top\" width=\"30\">" \
                  "<a href=\"https://instagram.com/happyfamily_hmao\" title=\"Instagram\" style=\"color:blue\">" \
                  "<img src=\"https://hf86.ru/img/icons/instagram.png\" height=\"20\">" \
                  "</a>" \
                  "</td>" \
                  "<td align=\"center\" valign=\"top\" width=\"30\">" \
                  "<a href=\"https://vk.com/happyfamily_hmao\" title=\"VK\" style=\"color:blue\">" \
                  "<img src=\"https://hf86.ru/img/icons/vk.png\" height=\"20\">" \
                  "</a>" \
                  "</td>" \
                  "<td align=\"center\" valign=\"top\" width=\"120\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"30\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" style=\"font-size:11px;line-height:16px;color:#585858;font" \
                  "-family:Arial, Helvetica, sans-serif;\">" \
                  "Copyright © 2020" \
                  "</td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "<td align=\"center\" valign=\"top\" width=\"20\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</body>" \
                  "</html>"
        subject_text = "Регистрация на сайте Happy Family"
    if subject == 'new_pass':
        message = "<!DOCTYPE html>" \
                  "<html lang=\"en\">" \
                  "<head>" \
                  "<link rel=\"icon\" href=\"https://hf86.ru/img/logo.ico\">" \
                  "<meta charset=\"UTF-8\">" \
                  "<title>Happy Family Surgut</title>" \
                  "<link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.3.1/css/all.css\" " \
                  "integrity=\"sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU\" " \
                  "crossorigin=\"anonymous\">" \
                  "</head>" \
                  "<body>" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\">" \
                  "<table width=\"640\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" width=\"600\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"15\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" width=\"95\" height=\"36\"><a href=\"https://hf86.ru\" " \
                  "target=\"_blank\"><img src=\"https://hf86.ru/img/logo.png\" width=\"95\" " \
                  "style=\"display:block;\" border=\"0\" alt=\"Happy Family\"></a>" \
                  "</td>" \
                  "<td align=\"right\" valign=\"middle\" style=\"font-family:Arial, Helvetica, " \
                  "sans-serif;font-size:12px;line-height:15px;color:#585858;\">" \
                  "HAPPY FAMILY SURGUT" \
                  "</td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"25\">" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" style=\"border:1px solid #dddddd;\" bgcolor=\"#ffffff\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  " <td align=\"left\" valign=\"top\" width=\"49\">" \
                  "</td>" \
                  "<td align=\"left\" valign=\"top\" width=\"500\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  " <tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"50\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" style=\"font-size:22px;line-height:28px;color:#333333;font" \
                  f"-weight:bold;font-family:Arial, Helvetica, sans-serif;\">Привет {email},</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td height=\"20\" align=\"left\" valign=\"top\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font" \
                  "-family:Arial, Helvetica, sans-serif;\">" \
                  "Вы только, что поменяли пароль на сайте <a href=\"https://hf86.ru\" target=\"_blank\" " \
                  "style=\"text-decoration:none;color:#585858;\"><span " \
                  "style=\"text-decoration:none;color:#585858;\">hf86.ru</span></a>." \
                  "<br><br>" \
                  "Для входа на сайт нажмите кнопку." \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td height=\"25\" align=\"left\" valign=\"top\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"50\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" width=\"126\"></td>" \
                  "<td align=\"center\" valign=\"middle\" height=\"50\" width=\"248\" bgcolor=\"#0082b2\" " \
                  "style=\"font-size:14px;line-height:19px;color:#ffffff;font-family:Arial, Helvetica, " \
                  "sans-serif;\"><a href=\"https://hf86.ru/enter/\" target=\"_blank\" " \
                  "style=\"color:#ffffff;text-decoration:none;\"><span " \
                  "style=\"font-size:14px;line-height:19px;color:#ffffff;font-family:Arial, Helvetica, " \
                  "sans-serif;\">ВОЙТИ</span></a></td>" \
                  "<td align=\"left\" valign=\"top\" width=\"126\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td height=\"30\" align=\"left\" valign=\"top\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td height=\"30\" align=\"left\" valign=\"top\" style=\"border-top:1px solid #dddddd;\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font" \
                  "-family:Arial, Helvetica, sans-serif;\">Спасибо, что Вы выбрали <a href=\"http://hf86.ru\" " \
                  "target=\"_blank\" style=\"text-decoration:none;color:#585858;\" rel=\" noopener " \
                  "noreferrer\"><span style=\"text-decoration:none;color:#585858;\">hf86.ru</span></a>. " \
                  "Удачи!<br><br>" \
                  "<strong>С уважением, команда Happy Family</strong>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"50\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "<td align=\"left\" valign=\"top\" width=\"49\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"40\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "<td align=\"center\" valign=\"top\" width=\"20\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "<table width=\"640\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" width=\"20\"></td>" \
                  "<td align=\"center\" valign=\"top\" width=\"600\">" \
                  "<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\"><a href=\"http://hf86.ru\" target=\"_blank\"><img " \
                  "src=\"https://hf86.ru/img/logo.png\" width=\"95\" border=\"0\" alt=\"Logo\"></a></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" style=\"font-size:14px;line-height:19px;color:#585858;font" \
                  "-family:Arial, Helvetica, sans-serif;\">" \
                  "Happy Family Surgut" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"20\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\">" \
                  "<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\">" \
                  "<tbody>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" width=\"120\"></td>" \
                  "<td align=\"center\" valign=\"top\" width=\"30\">" \
                  "<a href=\"https://instagram.com/happyfamily_hmao\" title=\"Instagram\" style=\"color:blue\">" \
                  "<img src=\"https://hf86.ru/img/icons/instagram.png\" height=\"20\">" \
                  "</a>" \
                  "</td>" \
                  "<td align=\"center\" valign=\"top\" width=\"30\">" \
                  "<a href=\"https://vk.com/happyfamily_hmao\" title=\"VK\" style=\"color:blue\">" \
                  "<img src=\"https://hf86.ru/img/icons/vk.png\" height=\"20\">" \
                  "</a>" \
                  "</td>" \
                  "<td align=\"center\" valign=\"top\" width=\"120\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"left\" valign=\"top\" height=\"30\"></td>" \
                  "</tr>" \
                  "<tr>" \
                  "<td align=\"center\" valign=\"top\" style=\"font-size:11px;line-height:16px;color:#585858;font" \
                  "-family:Arial, Helvetica, sans-serif;\">" \
                  "Copyright © 2020" \
                  "</td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "<td align=\"center\" valign=\"top\" width=\"20\"></td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</td>" \
                  "</tr>" \
                  "</tbody>" \
                  "</table>" \
                  "</body>" \
                  "</html>"
        subject_text = "Смена пароля на сайте Happy Family"

    send_mail(subject=subject_text, from_email=EMAIL_HOST_USER, recipient_list=[email],
              html_message=message, message=message)


def _get_error(txt):
    """ Возврат ошибки или сообщения """
    return mark_safe("<div class=\"m-alert m-alert--outline alert alert-danger alert-dismissible\" "
                     "role=\"alert\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" "
                     "aria-label=\"Close\"></button><span>" + txt + "</span></div>")


def _create_user(email, password):
    """ Создание нового пользователя """
    return Users.objects.create_user(email=email, password=password)


def _update_ref_counter(ref):
    """ Увеличение счетчика привлеченных пользователей на 1 для пользователя с указанным ref """
    Users.objects.annotate(email_md5=MD5('email')).annotate(ref_value=Right('email_md5', 8)).filter(
        ref_value=ref).values('ref').update(ref=F('ref') + 1)


def _get_user(email):
    """ Получение пользователя по email """
    return Users.objects.filter(email=email)


def _set_new_password(email, password):
    """ Установка нового пароля """
    user = Users.objects.get(email=email)
    user.set_password(password)
    user.reset = str(md5(f"{email}{password}".encode()).hexdigest())
    user.save()


def index(request):
    """ Главная страница """
    if request.user.is_authenticated:
        return redirect('LK')
    ref = request.GET.get('ref', None)
    forget = request.GET.get('forget', None)
    if ref is not None:
        if len(ref) != 8:
            ref = None
    if forget is not None:
        if len(forget) != 32:
            forget = None

    return render(request, 'HFadmin/admin.html', {'ref': ref, 'new': forget})


def logout_view(request):
    """ Закрытие сессии пользователя при выходе из ЛК с сохранением корзины """
    for key in list(request.session.keys()):
        if key != 'basket':
            del request.session[key]
    return redirect('../../')


def signin(request):
    """ Авторизация """
    if request.user.is_authenticated:
        return redirect('../../lk')

    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    if email is None or password is None:
        signup_err = _get_error('Введите email и пароль')
        return render(request, 'HFadmin/admin.html', {'signup_err': signup_err})

    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('../../lk')
    else:
        auth_err = _get_error('Неправильный email или пароль')
        return render(request, 'HFadmin/admin.html', {'auth_err': auth_err})


def signup(request):
    """ Регистрация """
    if request.user.is_authenticated:
        return redirect('../../lk')

    email = request.POST.get('email', None)
    password = request.POST.get('pass1', None)
    ref = request.POST.get('ref_id', None)
    if email is None or password is None:
        signup_err = _get_error('Введите email и пароль')
        return render(request, 'HFadmin/admin.html', {'signup_err': signup_err, 'ref': 'Referal (Option)'})

    created = _create_user(email, password)
    if created is not None:
        user = authenticate(request, username=email, password=password)
        if ref is not None:
            _update_ref_counter(ref)
        if user is not None:
            login(request, user)
            _send_email('', email, 'signup')
        return redirect('../../lk')
    else:
        signup_err = _get_error('Такой пользователь уже существует')
        return render(request, 'HFadmin/admin.html', {'signup_err': signup_err, 'ref': ref})


def reset_pass(request):
    """ Форма восстановление пароля """
    if request.user.is_authenticated:
        return redirect('../../lk')

    reset_err = _get_error('Неправильный email')
    if request.POST:
        email = request.POST.get('email', None)
        if email is None:
            return render(request, 'HFadmin/admin.html', {'reset_err': reset_err})

        user = _get_user(email).values('email', 'reset')
        if user:
            reset_err = _get_error('На указанный email отправлено письмо с указаниями по смене пароля!')
            _send_email(user, email, 'reset')
            return render(request, 'HFadmin/admin.html', {'reset_err': reset_err})
        else:
            reset_err = _get_error('Такого пользователя не существует')
            return render(request, 'HFadmin/admin.html', {'reset_err': reset_err})

    else:
        return render(request, 'HFadmin/admin.html', {'reset_err': reset_err})


def new_pass(request):
    """ Форма установка нового пароля """
    if request.user.is_authenticated:
        return redirect('../../lk')

    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    password_confirmation = request.POST.get('password_confirmation', None)

    if email is None or password is None:
        new_err = _get_error('Введите email и пароль')
        return render(request, 'HFadmin/admin.html', {'new_err': new_err, 'new': True})

    if password != password_confirmation:
        new_err = _get_error('Пароли не совпадают')
        return render(request, 'HFadmin/admin.html', {'new_err': new_err, 'new': True})

    user = _get_user(email)
    if user:
        new_err = _get_error('Пароль изменен. Пожалуйста авторизуйтесь')
        _set_new_password(email, password)
        _send_email('', email, 'new_pass')
        return render(request, 'HFadmin/admin.html', {'auth_err': new_err})
    else:
        new_err = _get_error('Такого пользователя не существует')
        return render(request, 'HFadmin/admin.html', {'new_err': new_err, 'new': True})
