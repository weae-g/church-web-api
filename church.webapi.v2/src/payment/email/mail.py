# Создадим роутер для отправки электронных писем с изображением
# Импорты
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL import Image, ImageDraw, ImageFont
from jinja2 import Template, Environment
import os


def send_payment_email_health(phone_number, note_type, user_email, note_name, from_name, user_name, note_cost, admin_email='spasskysobor.ru@mail.ru'):
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587
    smtp_username = 'spasskysobor.ru@mail.ru'
    smtp_password = '53YruktdKxupuebA2cJZ'
    
    admin_template = Template("""
    <html>
        <body>
            <p>Новый платеж получен:</p>
            <ul>
                <li>Имя покупателя: {{ from_name }}</li>
                <li>За кого: {{ user_name }}</li>
                <li>Email пользователя: {{ user_email }}</li>
                <li>Номер пользователя: {{ phone_number }}</li>
                <li>Тип требы: {{ note_type }}</li>
                <li>Наименование требы: {{ note_name }}</li>                
                <li>Стоимость требы: {{ note_cost }}</li>
            </ul>
        </body>
    </html>
    """)
    
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Сертификат</title>
</head>
<body>
    <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="min-height: 600px; width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #d4af37; border-radius: 1rem; background: #fff5e1; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="text-align: center; color: #d4af37; margin-bottom: 10px; line-height: 120%;">Уважаемый (-ая) {{ from_name }}. Благодарим вас за помощь, оказанную нашему храму. Подтверждаем, что нами получен ваш заказ на исполнение требы. С уважением, настоятель храма иеромонах Кирилл Забавнов.</div>
            <div style="content: ''; position: absolute; top: 10px; right: 10px; bottom: 10px; left: 10px; border: 1px dashed #e6b95b; border-radius: 8px; pointer-events: none;"></div>
            
           <div style="display: grid; gap: 1rem; grid-template-columns: repeat(1, 1fr);">
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem;">
                    <p style="text-align: center; margin: 0;">Русская Православная Церковь</p>
                    <p style="text-align: center; margin: 0;">Набережно-Челнинская епархия</p>
                </div>
                <div style="text-align: center;">
                    <img src="cid:logo" alt="Logo" style="width: 100%; max-width: 140px; min-width: 140px; height: auto; border-radius: 50%; filter: grayscale(1);">
                </div>
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem;">
                    <p style="text-align: center; margin: 0;">Татарстанская Митрополия</p>
                    <p style="text-align: center; margin: 0;">Казанская Епархия</p>
                </div>
            </div>
    
            <div style="text-align: center; font-size: 20px; color: #d4af37; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">Спасский собор г. Елабуги</div>
            <div style="text-align: center; font-size: 20px; color: #d4af37; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">{{ note_type }}</div>
            <div style="text-align: center; color: #d4af37; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">О здравии<div>
    
            <div style="display: flex; flex-direction: column; align-items: flex-start; width: calc(100% - 2rem); height: 100%; padding: 1rem; background: #fdfdfd; border-radius: 0.5rem; position: relative; z-index: 1;">
                {% for index, name in enumerate(note_names.split('\n'), start=1) %}
                <p style="font-family: 'Times New Roman', serif; font-size: 18px; line-height: 1.6; color: #333; text-align: center; margin: 5px 0;">{{ index }}. {{ name }}</p>
                {% endfor %}
            </div>
    
            <div style="width: 100%; display: flex; flex-direction: column; align-items: flex-end;">
                <p style="font-family: 'Times New Roman', serif; margin: 5px 0; font-size: 18px;">Сумма: {{ note_cost }} руб.</p>
            </div>
    
            <div style="text-align: center; padding: 1rem; background: #fff5e1; border-radius: 0.5rem; font-size: 18px;">
                <p style="margin: 0;">Контактная информация:</p>
                <a href="https://spasskysobor.ru/">Наш сайт</a>
                <p style="margin: 0;">Email: spasskysobor.ru@mail.ru</p>
                <p style="margin: 0;">Телефон: +7 (962) 578-26-65</p>
            </div>
        </div>
    
        <div style="width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #d4af37; border-radius: 1rem; background: #fff5e1; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="padding: 1rem; background: #fdf8e4; border-radius: 0.5rem; text-align: left;">
                <p style="font-family: 'Times New Roman', serif; margin: 5px 0; font-size: 14px;">Ваша заявка на требу принята системой сбора добровольных пожертвований и контроля исполнения треб.</p>
                <p style="font-family: 'Times New Roman', serif; margin: 5px 0; font-size: 14px;">О получении Вашей благотворительной помощи храмом и о начале исполнения требы Вам будет сообщено отдельным письмом.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

    env = Environment()
    env.globals['enumerate'] = enumerate

    user_template = env.from_string(html_content)
    
    admin_msg = MIMEMultipart()
    admin_msg['Subject'] = 'Новый платеж получен'
    admin_msg['From'] = smtp_username
    admin_msg['To'] = admin_email
    admin_msg.attach(MIMEText(admin_template.render(
        user_name=user_name,
        note_type=note_type,
        from_name=from_name,
        note_cost=note_cost,
        note_name=note_name,
        user_email=user_email,
        phone_number=phone_number
    ), 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(admin_msg)
    
    user_msg = MIMEMultipart()
    user_msg['Subject'] = 'От Спасского собора г. Елабуга о благодарности!'
    user_msg['From'] = smtp_username
    user_msg['To'] = user_email

    html_part = MIMEText(user_template.render(
        note_type=note_type,
        note_name=note_name,
        from_name=from_name,
        note_names=f'{user_name}',
        note_cost=note_cost
    ), 'html')
    user_msg.attach(html_part)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, 'logo.png')

    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_image = MIMEImage(logo_data, name='logo.png')
    logo_image.add_header('Content-ID', '<logo>')
    user_msg.attach(logo_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(user_msg)


def send_payment_email_rest(phone_number,note_type,user_email, note_name, from_name, user_name, note_cost, admin_email='spasskysobor.ru@mail.ru'):
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587
    smtp_username = 'spasskysobor.ru@mail.ru'
    smtp_password = '53YruktdKxupuebA2cJZ'
    
    # Шаблон для письма админу
    admin_template = Template("""
    <html>
        <body>
            <p>Новый платеж получен:</p>
            <ul>
                <li>Имя покупателя: {{ from_name }}</li>
                <li>За кого: {{ user_name }}</li>
                <li>Email пользователя: {{ user_email }}</li>
                <li>Номер пользователя: {{ phone_number }}</li> 
                <li>Тип требы: {{ note_type }}</li>
                <li>Наименование требы: {{ note_name }}</li>                
                <li>Стоимость требы: {{ note_cost }}</li>
            </ul>
        </body>
    </html>
    """)
    

    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Сертификат</title>
</head>
<body>
    <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style=" min-height: 600px; width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #b9b9b9; border-radius: 1rem; background: #f3f3f3; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="text-align: center; color: #d4af37; margin-bottom: 10px; line-height: 120%;">Уважаемый (-ая) {{ from_name }}. Благодарим вас за помощь, оказанную нашему храму. Подтверждаем, что нами получен ваш заказ на исполнение требы. С уважением, настоятель храма иеромонах Кирилл Забавнов.</div>
            <div style="content: ''; position: absolute; top: 10px; right: 10px; bottom: 10px; left: 10px; border: 1px dashed #868686; border-radius: 8px; pointer-events: none;"></div>
    
            <div style="display: grid; gap: 1rem; grid-template-columns: repeat(1, 1fr);">
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem;">
                    <p style="text-align: center; margin: 0;">Русская Православная Церковь</p>
                    <p style="text-align: center; margin: 0;">Московский Патриархат</p>
                </div>
                <div style="text-align: center;">
                    <img src="cid:logo" alt="Logo" style="width: 100%; max-width: 140px; min-width: 140px; height: auto; border-radius: 50%; filter: grayscale(1);">
                </div>
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem;">
                    <p style="text-align: center; margin: 0;">Татарстанская Митрополия</p>
                    <p style="text-align: center; margin: 0;">Набережно-Челнинская епархия</p>
                </div>
            </div>
    
            <div style="text-align: center; font-size: 20px; color: #292929; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">Спасский собор г. Елабуги</div>
            <div style="text-align: center; font-size: 20px; color: #292929; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">{{ note_type }}</div>
            <div style="text-align: center; color: #292929; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">О упокоении<div>
    
            <div style="display: flex; flex-direction: column; align-items: flex-start; width: calc(100% - 2rem); height: 100%; padding: 1rem; background: #fdfdfd; border-radius: 0.5rem; position: relative; z-index: 1;">
                {% for index, name in enumerate(note_names.split('\n'), start=1) %}
                <p style="font-family: 'Times New Roman', serif; font-size: 18px; line-height: 1.6; color: #333; text-align: center; margin: 5px 0;">{{ index }}. {{ name }}</p>
                {% endfor %}
            </div>
    
            <div style="width: 100%; display: flex; flex-direction: column; align-items: flex-end;">
                <p style="font-family: 'Times New Roman', serif; margin: 5px 0; font-size: 18px;">Сумма: {{ note_cost }} руб.</p>
            </div>
    
            <div style="text-align: center; padding: 1rem; background: #fdfdfd; border-radius: 0.5rem; font-size: 18px;">
                <p style="margin: 0;">Контактная информация:</p>
                <a href="https://spasskysobor.ru/">Наш сайт</a>
                <p style="margin: 0;">Email: spasskysobor.ru@mail.ru</p>
                <p style="margin: 0;">Телефон: +7 (962) 578-26-65</p>
            </div>
        </div>
    
        <div style="width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #b9b9b9; border-radius: 1rem; background: #f3f3f3; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="padding: 1rem; background: #fdfdfd; border-radius: 0.5rem; text-align: left;">
                <p style="font-family: 'Times New Roman', serif; margin: 5px 0; font-size: 14px;">Ваша заявка на требу принята системой сбора добровольных пожертвований и контроля исполнения треб.</p>
                <p style="font-family: 'Times New Roman', serif; margin: 5px 0; font-size: 14px;">О получении Вашей благотворительной помощи храмом о начале исполнения требу Вам будет сообщено отдельным письмом.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


    env = Environment()
    env.globals['enumerate'] = enumerate

    user_template = env.from_string(html_content)
    

    admin_msg = MIMEMultipart()
    admin_msg['Subject'] = 'Новый платеж получен'
    admin_msg['From'] = smtp_username
    admin_msg['To'] = admin_email
    admin_msg.attach(MIMEText(admin_template.render
                              (user_name=user_name,note_type=note_type,from_name=from_name,
                               note_cost=note_cost, note_name=note_name, user_email=user_email, 
                               phone_number=phone_number), 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(admin_msg)
    


    user_msg = MIMEMultipart()
    user_msg['Subject'] = f'От Спасского собора г. Елабуга о благодарности!'
    user_msg['From'] = smtp_username
    user_msg['To'] = user_email
    #mrronal
    #fox.334

    html_part = MIMEText(user_template.render(note_type=note_type, note_name=note_name, from_name=from_name, note_names=f'{user_name}', note_cost=note_cost), 'html')
    user_msg.attach(html_part)
    

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, 'logo.png')

    # Добавление логотипа в письмо
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_image = MIMEImage(logo_data, name='logo.png')
    logo_image.add_header('Content-ID', '<logo>')
    user_msg.attach(logo_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(user_msg)


def send_payment_email_donation(user_name, cost, user_email, phone_number, donation, admin_email='spasskysobor.ru@mail.ru'):
  
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587
    smtp_username = 'spasskysobor.ru@mail.ru'
    smtp_password = '53YruktdKxupuebA2cJZ'
    

    admin_template = Template("""
    <html>
        <body>
            <p>Новый платеж получен:</p>
            <ul>
                <li>Имя покупателя: {{ user_name }}</li>
                <li>Сумма: {{ cost }}</li>
                <li>Email пользователя: {{ user_email }}</li>
                <li>Номер телефона: {{ phone_number }}</li>
                <li>Пожелания: {{ donation }}</li>
            </ul>
        </body>
    </html>
    """)
    
   
    html_content = """
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>Сертификат Благодарности</title>
  </head>
  <body style="font-family: 'Times New Roman', serif; margin: 0; padding: 0; background-color: #f8f8f8; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <div style="min-height: 600px; width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #d4af37; border-radius: 1rem; background: #fff5e1; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="text-align: center; color: #d4af37; margin-bottom: 10px; line-height: 120%;">Уважаемый (-ая) {{ from_name }}. Благодарим вас за помощь, оказанную нашему храму. С уважением, настоятель храма иеромонах Кирилл Забавнов.</div>
      <div style="position: absolute; top: 10px; right: 10px; bottom: 10px; left: 10px; border: 1px dashed #e6b95b; border-radius: 8px; pointer-events: none;"></div>

      <div style="display: grid; gap: 0.5rem; grid-template-columns: repeat(1, 1fr); text-align: center;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p style="margin: 0;">Русская Православная Церковь</p>
          <p style="margin: 0;">Московский Патриархат</p>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <img src="cid:logo" alt="Logo" style="width: 100%; max-width: 140px; min-width: 140px; height: auto; border-radius: 50%; filter: grayscale(1);" />
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p style="margin: 0;">Татарстанская Митрополия</p>
          <p style="margin: 0;">Набережно-Челнинская епархия</p>
        </div>
      </div>

      <div style="text-align: center; font-size: 20px; color: #d4af37; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">Спасский собор г. Елабуги</div>

      <div style="font-size: 24px; color: #d4af37; text-align: center;">
        <p style="margin: 0;">{{ cost }} руб.</p>
      </div>

      <div style="padding: 1rem; background: #fdf8e4; border-radius: 0.5rem; text-align: left;">
        <p style="text-align: center; font-size: 17px; margin: 5px 0;">
          Благодарим Вас за совершенное пожертвование. Ваш вклад поможет нам в осуществлении нашей задача и поддержке деятельности храма.
        </p>
      </div>

      <div style="text-align: center; padding: 1rem; background: #fff5e1; border-radius: 0.5rem; font-size: 18px; display: flex; flex-direction: column; gap: .5rem;">
        <p style="margin: 0;">Контактная информация:</p>
        <a href="https://spasskysobor.ru/" style="margin: 0;">Наш сайт</a>
        <p style="margin: 0;">Email: spasskysobor.ru@mail.ru</p>
        <p style="margin: 0;">Телефон: +7 (962) 578-26-65</p>
      </div>
    </div>
  </body>
</html>
"""

    env = Environment()
    env.globals['enumerate'] = enumerate


    user_template = env.from_string(html_content)
    

    admin_msg = MIMEMultipart()
    admin_msg['Subject'] = 'Новый платеж получен'
    admin_msg['From'] = smtp_username
    admin_msg['To'] = admin_email
    admin_msg.attach(MIMEText(admin_template.render(user_name=user_name, cost=cost, user_email=user_email, phone_number=phone_number, donation=donation), 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(admin_msg)
    
  
    user_msg = MIMEMultipart()
    user_msg['Subject'] = 'От Спасского собора г. Елабуга о благодарности!'
    user_msg['From'] = smtp_username
    user_msg['To'] = user_email
    
    html_part = MIMEText(user_template.render(cost=cost, note_names=f'{user_name}'), 'html')
    user_msg.attach(html_part)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, 'logo.png')


    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_image = MIMEImage(logo_data, name='logo.png')
    logo_image.add_header('Content-ID', '<logo>')
    user_msg.attach(logo_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(user_msg)

def send_payment_about(user_name, cost, user_email, note_name, admin_email='spasskysobor.ru@mail.ru'):
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587
    smtp_username = 'spasskysobor.ru@mail.ru'
    smtp_password = '53YruktdKxupuebA2cJZ'
    
    admin_template = Template("""
    <html>
        <body>
            <p>Письмо о завершении требы успешно отправлено!</p>
            <ul>
                <li>Имя покупателя: {{ user_name }}</li>
                <li>Сумма: {{ cost }}</li>
                <li>Email пользователя: {{ user_email }}</li>
                <li>Номер телефона: {{ note_name }}</li>
            </ul>
        </body>
    </html>
    """)
    
    html_content = """
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>Сертификат об окончании требы</title>
  </head>
  <body style="font-family: 'Times New Roman', serif; margin: 0; padding: 0; background-color: #f8f8f8; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
  <div style="min-height: 600px; width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #d4af37; border-radius: 1rem; background: #fff5e1; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="text-align: center; color: #d4af37; margin-bottom: 10px; line-height: 120%;">Уважаемый (-ая) {{ user_name }}. Благодарим вас за помощь, оказанную нашему храму. Подтверждаем что ваш заказ на исполнение требы исполнен. С уважением, настоятель храма иеромонах Кирилл Забавнов.</div>
      <div style="content: ''; position: absolute; top: 10px; right: 10px; bottom: 10px; left: 10px; border: 1px dashed #e6b95b; border-radius: 8px; pointer-events: none;"></div>
      <div style="display: grid; gap: 0.5rem; grid-template-columns: repeat(1, 1fr); text-align: center;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p>Русская Православная Церковь</p>
          <p>Московский Патриархат</p>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <img src="cid:logo" alt="Logo" style="width: 100%; max-width: 140px; min-width: 140px; height: auto; border-radius: 50%; filter: grayscale(1);" />
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p>Татарстанская Митрополия</p>
          <p>Набережно-Челнинская епархия</p>
        </div>
      </div>
      <div style="text-align: center; font-size: 20px; color: #d4af37; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">Спасский собор г. Елабуги</div>
      <div style="padding: 1rem; background: #fdf8e4; border-radius: 0.5rem; text-align: left;">
        <p style="text-align: center; font-size: 17px; margin: 5px 0;">
          Благодарим Вас за помощь приходу. Ваша заявка выполнена. Мы ценим Ваш вклад и поддержку.
        </p>
      </div>
      <div style="text-align: center; padding: 1rem; background: #fff5e1; border-radius: 0.5rem; font-size: 18px; display: flex; flex-direction: column; gap: .5rem;">
        <p>Контактная информация:</p>
        <a href="https://spasskysobor.ru/" style="margin: 0;">Наш сайт</a>
        <p style="margin: 0;">Email: spasskysobor.ru@mail.ru</p>
        <p style="margin: 0;">Телефон: +7 (962) 578-26-65</p>
      </div>
    </div>
  </body>
</html>
"""
 
    env = Environment()
    env.globals['enumerate'] = enumerate

    # Компиляция шаблона
    user_template = env.from_string(html_content)
    
    admin_msg = MIMEMultipart()
    admin_msg['Subject'] = 'Письмо о окончании требы'
    admin_msg['From'] = smtp_username
    admin_msg['To'] = admin_email
    admin_msg.attach(MIMEText(admin_template.render(user_name=user_name, cost=cost, user_email=user_email, note_name=note_name), 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(admin_msg)
    
    user_msg = MIMEMultipart()
    user_msg['Subject'] = 'От Спасского собора г. Елабуга об окончании требы!'
    user_msg['From'] = smtp_username
    user_msg['To'] = user_email
    
    html_part = MIMEText(user_template.render(cost=cost, note_names=f'{user_name}', user_name=user_name), 'html')
    user_msg.attach(html_part)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, 'logo.png')

    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_image = MIMEImage(logo_data, name='logo.png')
    logo_image.add_header('Content-ID', '<logo>')
    user_msg.attach(logo_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(user_msg)

def send_payment_about_candle(user_name, cost, user_email, note_name, admin_email='spasskysobor.ru@mail.ru'):
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587
    smtp_username = 'spasskysobor.ru@mail.ru'
    smtp_password = '53YruktdKxupuebA2cJZ'
    
    admin_template = Template("""
    <html>
        <body>
            <p>Письмо о свечи успешно отправлено!</p>
            <ul>
                <li>Имя покупателя: {{ user_name }}</li>
                <li>Сумма: {{ cost }}</li>
                <li>Email пользователя: {{ user_email }}</li>
                <li>Номер телефона: {{ note_name }}</li>
            </ul>
        </body>
    </html>
    """)
    
    html_content = """
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>Сертификат о свечи требы</title>
  </head>
  <body style="font-family: 'Times New Roman', serif; margin: 0; padding: 0; background-color: #f8f8f8; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
  <div style="min-height: 600px; width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #d4af37; border-radius: 1rem; background: #fff5e1; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="text-align: center; color: #d4af37; margin-bottom: 10px; line-height: 120%;">Уважаемый (-ая) {{ user_name }}. Благодарим вас за помощь, оказанную нашему храму. Подтверждаем что ваш заказ на свечку исполнен. С уважением, настоятель храма иеромонах Кирилл Забавнов.</div>
      <div style="content: ''; position: absolute; top: 10px; right: 10px; bottom: 10px; left: 10px; border: 1px dashed #e6b95b; border-radius: 8px; pointer-events: none;"></div>
      <div style="display: grid; gap: 0.5rem; grid-template-columns: repeat(1, 1fr); text-align: center;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p>Русская Православная Церковь</p>
          <p>Московский Патриархат</p>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <img src="cid:logo" alt="Logo" style="width: 100%; max-width: 140px; min-width: 140px; height: auto; border-radius: 50%; filter: grayscale(1);" />
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p>Татарстанская Митрополия</p>
          <p>Набережно-Челнинская епархия</p>
        </div>
      </div>
      <div style="text-align: center; font-size: 20px; color: #d4af37; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">Спасский собор г. Елабуги</div>
      <div style="padding: 1rem; background: #fdf8e4; border-radius: 0.5rem; text-align: left;">
        <p style="text-align: center; font-size: 17px; margin: 5px 0;">
          Благодарим Вас за помощь приходу. Ваша заявка выполнена. Мы ценим Ваш вклад и поддержку.
        </p>
      </div>
      <div style="text-align: center; padding: 1rem; background: #fff5e1; border-radius: 0.5rem; font-size: 18px; display: flex; flex-direction: column; gap: .5rem;">
        <p>Контактная информация:</p>
        <a href="https://spasskysobor.ru/" style="margin: 0;">Наш сайт</a>
        <p style="margin: 0;">Email: spasskysobor.ru@mail.ru</p>
        <p style="margin: 0;">Телефон: +7 (962) 578-26-65</p>
      </div>
    </div>
  </body>
</html>
"""
 
    env = Environment()
    env.globals['enumerate'] = enumerate

    # Компиляция шаблона
    user_template = env.from_string(html_content)
    
    admin_msg = MIMEMultipart()
    admin_msg['Subject'] = 'Письмо о окончании требы'
    admin_msg['From'] = smtp_username
    admin_msg['To'] = admin_email
    admin_msg.attach(MIMEText(admin_template.render(user_name=user_name, cost=cost, user_email=user_email, note_name=note_name), 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(admin_msg)
    
    user_msg = MIMEMultipart()
    user_msg['Subject'] = 'От Спасского собора г. Елабуга об окончании требы!'
    user_msg['From'] = smtp_username
    user_msg['To'] = user_email
    
    html_part = MIMEText(user_template.render(cost=cost, note_names=f'{user_name}', user_name=user_name), 'html')
    user_msg.attach(html_part)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, 'logo.png')

    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_image = MIMEImage(logo_data, name='logo.png')
    logo_image.add_header('Content-ID', '<logo>')
    user_msg.attach(logo_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(user_msg)


def send_payment_about_start(user_name, cost, user_email, note_name, admin_email='spasskysobor.ru@mail.ru'):
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587
    smtp_username = 'spasskysobor.ru@mail.ru'
    smtp_password = '53YruktdKxupuebA2cJZ'
    
    admin_template = Template("""
    <html>
        <body>
            <p>Письмо о взятие в работу требы успешно отправлено!</p>
            <ul>
                <li>Имя покупателя: {{ user_name }}</li>
                <li>Сумма: {{ cost }}</li>
                <li>Email пользователя: {{ user_email }}</li>
                <li>Номер телефона: {{ note_name }}</li>
            </ul>
        </body>
    </html>
    """)
    
    html_content = """
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>Сертификат о начале требы</title>
  </head>
  <body style="font-family: 'Times New Roman', serif; margin: 0; padding: 0; background-color: #f8f8f8; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
  <div style="min-height: 600px; width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #d4af37; border-radius: 1rem; background: #fff5e1; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="text-align: center; color: #d4af37; margin-bottom: 10px; line-height: 120%;">Уважаемый (-ая) {{ user_name }}. Благодарим вас за помощь, оказанную нашему храму. Подтверждаем что ваш заказ на исполнение требы был взят в работу. С уважением, настоятель храма иеромонах Кирилл Забавнов.</div>
      <div style="content: ''; position: absolute; top: 10px; right: 10px; bottom: 10px; left: 10px; border: 1px dashed #e6b95b; border-radius: 8px; pointer-events: none;"></div>
      <div style="display: grid; gap: 0.5rem; grid-template-columns: repeat(1, 1fr); text-align: center;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p>Русская Православная Церковь</p>
          <p>Московский Патриархат</p>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <img src="cid:logo" alt="Logo" style="width: 100%; max-width: 140px; min-width: 140px; height: auto; border-radius: 50%; filter: grayscale(1);" />
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p>Татарстанская Митрополия</p>
          <p>Набережно-Челнинская епархия</p>
        </div>
      </div>
      <div style="text-align: center; font-size: 20px; color: #d4af37; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">Спасский собор г. Елабуги</div>
      <div style="padding: 1rem; background: #fdf8e4; border-radius: 0.5rem; text-align: left;">
        <p style="text-align: center; font-size: 17px; margin: 5px 0;">
          Ваша заявка принята, и находится на стадии исполнения. Мы ценим Ваш вклад и поддержку.
        </p>
      </div>
      <div style="text-align: center; padding: 1rem; background: #fff5e1; border-radius: 0.5rem; font-size: 18px; display: flex; flex-direction: column; gap: .5rem;">
        <p>Контактная информация:</p>
        <a href="https://spasskysobor.ru/" style="margin: 0;">Наш сайт</a>
        <p style="margin: 0;">Email: spasskysobor.ru@mail.ru</p>
        <p style="margin: 0;">Телефон: +7 (962) 578-26-65</p>
      </div>
    </div>
  </body>
</html>
"""
 
    env = Environment()
    env.globals['enumerate'] = enumerate

    # Компиляция шаблона
    user_template = env.from_string(html_content)
    
    admin_msg = MIMEMultipart()
    admin_msg['Subject'] = 'Письмо о окончании требы'
    admin_msg['From'] = smtp_username
    admin_msg['To'] = admin_email
    admin_msg.attach(MIMEText(admin_template.render(user_name=user_name, cost=cost, user_email=user_email, note_name=note_name), 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(admin_msg)
    
    user_msg = MIMEMultipart()
    user_msg['Subject'] = 'От Спасского собора г. Елабуга о начале исполнения требы!'
    user_msg['From'] = smtp_username
    user_msg['To'] = user_email
    
    html_part = MIMEText(user_template.render(cost=cost, note_names=f'{user_name}', user_name=user_name), 'html')
    user_msg.attach(html_part)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, 'logo.png')

    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_image = MIMEImage(logo_data, name='logo.png')
    logo_image.add_header('Content-ID', '<logo>')
    user_msg.attach(logo_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(user_msg)


def send_payment_email_candle(user_name, cost, user_email, phone_number, candle_type, candle_icon, candle_prayer, admin_email='spasskysobor.ru@mail.ru'):
    # SMTP сервер конфигурация
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587
    smtp_username = 'spasskysobor.ru@mail.ru'
    smtp_password = '53YruktdKxupuebA2cJZ'
    
    # Шаблон для письма админу
    admin_template = Template("""
    <html>
        <body>
            <p>Новый заказ на свечу получен:</p>
            <ul>
                <li>Имя покупателя: {{ user_name }}</li>
                <li>Сумма: {{ cost }}</li>
                <li>Email пользователя: {{ user_email }}</li>
                <li>Номер телефона: {{ phone_number }}</li>
                <li>Тип свечи: {{ candle_type }}</li>
                <li>Икона: {{ candle_icon }}</li>
                <li>Молитва: {{ candle_prayer }}</li>
            </ul>
        </body>
    </html>
    """)
    
    # HTML-шаблон для письма пользователю с инлайн-стилями
    html_content = """
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>Сертификат Благодарности</title>
  </head>
  <body style="font-family: 'Times New Roman', serif; margin: 0; padding: 0; background-color: #f8f8f8; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <div style="min-height: 600px; width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #d4af37; border-radius: 1rem; background: #fff5e1; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="text-align: center; color: #d4af37; margin-bottom: 10px; line-height: 120%;">Уважаемый (-ая) {{ from_name }}. Благодарим вас за помощь, оказанную нашему храму. Подтверждаем, что нами получен ваш заказ на свечу. С уважением, настоятель храма иеромонах Кирилл Забавнов.</div>
      <div style="position: absolute; top: 10px; right: 10px; bottom: 10px; left: 10px; border: 1px dashed #e6b95b; border-radius: 8px; pointer-events: none;"></div>
   

      <div style="display: grid; gap: 0.5rem; grid-template-columns: repeat(1, 1fr); text-align: center;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p style="margin: 0;">Русская Православная Церковь</p>
          <p style="margin: 0;">Московский Патриархат</p>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <img src="cid:logo" alt="Logo" style="width: 100%; max-width: 140px; min-width: 140px; height: auto; border-radius: 50%; filter: grayscale(1);" />
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p style="margin: 0;">Татарстанская Митрополия</p>
          <p style="margin: 0;">Набережно-Челнинская епархия</p>
        </div>
      </div>

      <div style="text-align: center; font-size: 20px; color: #d4af37; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">Спасский собор г. Елабуги</div>

      <div style="font-size: 24px; color: #d4af37; text-align: center;">
        <p style="margin: 0;">{{ cost }} руб.</p>
      </div>

      <div style="padding: 1rem; background: #fdf8e4; border-radius: 0.5rem; text-align: left;">
        <p style="text-align: center; font-size: 17px; margin: 5px 0;">
          Благодарим Вас за заказ свечи. Ваш вклад поможет нам в осуществлении нашей задача и поддержке деятельности храма.
        </p>
      </div>

      <div style="text-align: center; padding: 1rem; background: #fff5e1; border-radius: 0.5rem; font-size: 18px; display: flex; flex-direction: column; gap: .5rem;">
        <p style="margin: 0;">Контактная информация:</p>
        <a href="https://spasskysobor.ru/" style="margin: 0;">Наш сайт</a>
        <p style="margin: 0;">Email: spasskysobor.ru@mail.ru</p>
        <p style="margin: 0;">Телефон: +7 (962) 578-26-65</p>
      </div>
    </div>
  </body>
</html>
"""
    # Создание окружения Jinja2 и добавление enumerate
    env = Environment()
    env.globals['enumerate'] = enumerate

    # Компиляция шаблона
    user_template = env.from_string(html_content)
    
    # Создание и отправка письма админу
    admin_msg = MIMEMultipart()
    admin_msg['Subject'] = 'Новый заказ на свечу получен'
    admin_msg['From'] = smtp_username
    admin_msg['To'] = admin_email
    admin_msg.attach(MIMEText(admin_template.render(user_name=user_name, cost=cost, user_email=user_email, phone_number=phone_number, candle_type=candle_type, candle_icon=candle_icon, candle_prayer=candle_prayer), 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(admin_msg)
    
    # Создание и отправка письма пользователю
    user_msg = MIMEMultipart()
    user_msg['Subject'] = 'От Спасского собора г. Елабуга о заказе свечи!'
    user_msg['From'] = smtp_username
    user_msg['To'] = user_email
    
    html_part = MIMEText(user_template.render(cost=cost, note_names=f'{user_name}'), 'html')
    user_msg.attach(html_part)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, 'logo.png')

    # Добавление логотипа в письмо
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_image = MIMEImage(logo_data, name='logo.png')
    logo_image.add_header('Content-ID', '<logo>')
    user_msg.attach(logo_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(user_msg)


def send_payment_email_brick(user_name, cost, user_email, message, color, admin_email='spasskysobor.ru@mail.ru'):
    # SMTP сервер конфигурация
    smtp_server = 'smtp.mail.ru'
    smtp_port = 587
    smtp_username = 'spasskysobor.ru@mail.ru'
    smtp_password = '53YruktdKxupuebA2cJZ'
    
    # Шаблон для письма админу
    admin_template = Template("""
    <html>
        <body>
            <p>Новый заказ на кирпичик получен:</p>
            <ul>
                <li>Имя покупателя: {{ user_name }}</li>
                <li>Сумма: {{ cost }}</li>
                <li>Email пользователя: {{ user_email }}</li>
                <li>Сообщение: {{ message }}</li>
                <li>Цвет: {{ color }}</li>
            </ul>
        </body>
    </html>
    """)

    # HTML-шаблон для письма пользователю с инлайн-стилями
    html_content = """
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>Сертификат Благодарности</title>
  </head>
  <body style="font-family: 'Times New Roman', serif; margin: 0; padding: 0; background-color: #f8f8f8; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
   <div style="min-height: 600px; width: calc(100% - 42px); height: 100%; padding: 20px; border: 1px solid #d4af37; border-radius: 1rem; background: #fff5e1; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Times New Roman', serif; display: flex; flex-direction: column; gap: 1rem; position: relative;">
            <div style="text-align: center; color: #d4af37; margin-bottom: 10px; line-height: 120%;">Уважаемый (-ая) {{ user_name }}. Благодарим вас за помощь, оказанную нашему храму. Подтверждаем, что нами получен ваш заказ на кирпичик. С уважением, настоятель храма иеромонах Кирилл Забавнов.</div>
      <div style="position: absolute; top: 10px; right: 10px; bottom: 10px; left: 10px; border: 1px dashed #e6b95b; border-radius: 8px; pointer-events: none;"></div>

      <div style="display: grid; gap: 0.5rem; grid-template-columns: repeat(1, 1fr); text-align: center;">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p style="margin: 0;">Русская Православная Церковь</p>
          <p style="margin: 0;">Московский Патриархат</p>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <img src="cid:logo" alt="Logo" style="width: 100%; max-width: 140px; min-width: 140px; height: auto; border-radius: 50%; filter: grayscale(1);" />
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; font-size: 17px;">
          <p style="margin: 0;">Татарстанская Митрополия</p>
          <p style="margin: 0;">Набережно-Челнинская епархия</p>
        </div>
      </div>

      <div style="text-align: center; font-size: 20px; color: #d4af37; margin-bottom: 10px; line-height: 120%; text-transform: uppercase;">Спасский собор г. Елабуги</div>

      <div style="font-size: 24px; color: #d4af37; text-align: center;">
        <p style="margin: 0;">{{ cost }} руб.</p>
      </div>

      <div style="padding: 1rem; background: #fdf8e4; border-radius: 0.5rem; text-align: left;">
        <p style="text-align: center; font-size: 17px; margin: 5px 0;">
          Благодарим Вас за заказ кирпичика. Ваш вклад поможет нам в осуществлении нашей задача и поддержке деятельности храма.
        </p>
      </div>

      <div style="text-align: center; padding: 1rem; background: #fff5e1; border-radius: 0.5rem; font-size: 18px; display: flex; flex-direction: column; gap: .5rem;">
        <p style="margin: 0;">Контактная информация:</p>
        <a href="https://spasskysobor.ru/" style="margin: 0;">Наш сайт</a>
        <p style="margin: 0;">Email: spasskysobor.ru@mail.ru</p>
        <p style="margin: 0;">Телефон: +7 (962) 578-26-65</p>
      </div>
    </div>
  </body>
</html>
"""
    # Создание окружения Jinja2 и добавление enumerate
    env = Environment()
    env.globals['enumerate'] = enumerate

    # Компиляция шаблона
    user_template = env.from_string(html_content)

    # Создание и отправка письма админу
    admin_msg = MIMEMultipart()
    admin_msg['Subject'] = 'Новый заказ на кирпичик получен'
    admin_msg['From'] = smtp_username
    admin_msg['To'] = admin_email
    admin_msg.attach(MIMEText(admin_template.render(user_name=user_name, cost=cost, user_email=user_email, message=message, color=color), 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(admin_msg)
    
    # Создание и отправка письма пользователю
    user_msg = MIMEMultipart()
    user_msg['Subject'] = 'От Спасского собора г. Елабуга о заказе кирпичика!'
    user_msg['From'] = smtp_username
    user_msg['To'] = user_email
    
    html_part = MIMEText(user_template.render(cost=cost, user_name=user_name), 'html')
    user_msg.attach(html_part)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, 'logo.png')

    # Добавление логотипа в письмо
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo_image = MIMEImage(logo_data)
    logo_image.add_header('Content-ID', '<logo>')
    user_msg.attach(logo_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(user_msg)


# Тестовые данные

#fox.334@mail.ru

user_email = 'fox.334@mail.ru'
from_name = 'Анна'
user_name = 'Иван Иванов\nИванов Иван'
phone_number = '89674638251'
payment_info = 'Оплата услуги №12345'
admin_email = 'spasskysobor.ru@mail.ru'
note_cost = '100'
note_name = 'Обедня'
note_type = 'За упокоение'
donation = 'Всех благ!!!'

# Запуск теста переделать
#send_payment_email_candle(from_name, note_cost, user_email, phone_number, note_type, "Икноа", "Свеча 80")
#send_payment_email_donation(from_name, note_cost, user_email,phone_number, donation)
# Просмотреть

#send_payment_about_start(from_name, note_cost, user_email, "За здравие")
#send_payment_about(from_name, note_cost, user_email, "За здравие")
#send_payment_email_brick(from_name, note_cost, user_email, "Здравствуйте", "color")

#send_payment_email_rest(phone_number,note_type, user_email,note_name, from_name, user_name, note_cost)
print("Test email sent successfully.")
