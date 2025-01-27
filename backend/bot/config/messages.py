START_MESSAGE: str = """\
Привет, <b>{full_name}!</b>

Добро пожаловать в VPN который никогда не зависает

📲 Качественные сервера
🚀 Самая высокая скорость
💃🏿 Доступ по всему миру
💳 Оплата картой РФ и USDT

🏅Никаких просадок связи, 1 сервер = 10 устройств

👬 Пригласите друга/подругу и заработай 80₽ за каждого. Ваши друзья получат 100₽ на баланс!
⬇️ ⬇️  Жмите кнопку!  ⬇️ ⬇️\
"""

TARIFFS_MENU: str = """\
<blockquote>💵 Тарифы</blockquote>

Вот список действующих тарифов. Выбирайте понравившийся\
"""

TARIFF_PAYMENT: str = """\
Выбран тариф: {title} - {price} руб.
Проведите оплату в мини-приложении по кнопке «Оплатить»

<b>После оплаты в мини-приложении нажмите на кнопку «✅ Готово»</b>\
"""

TARIFF_PAYMENT_BALANCE: str = """\
Выбран тариф: {title} - {price} руб.
Проведите оплату в мини-приложении по кнопке «Оплатить»

Также Вы можете купить конфиг, списав средства с Вашего <b>баланса</b>, \
нажав на кнопку <b>«Списать с баланса»</b>

<b>После оплаты в мини-приложении нажмите на кнопку «✅ Готово»</b>\
"""

TARIFF_PAYMENT_DONE: str = """\
✅ Оплата проведена успешно!

Ваш конфиг: {config_name}
Активен до: {expiring_at}\
"""

FAILED_TO_INIT_PAYMENT: str = """\
❌ Не удалось создать чек для оплаты!
Пожалуйста, свяжитесь с поддержкой и опишите \
ситуацию указав на вышеописанную причину\
"""

FAILED_TO_CHECK_PAYMENT: str = """\
❌ Не удалось получить статус платежа!
Пожалуйста, свяжитесь с поддержкой и опишите \
ситуацию указав на вышеописанную причину\
"""

FAILED_TO_PAY_BALANCE: str = """\
❌ Недостаточно средств на балансе!\
"""

FAILED_TO_CANCEL_PAYMENT: str = """\
❌ Не удалось отменить платеж!
Пожалуйста, свяжитесь с поддержкой и опишите \
ситуацию указав на вышеописанную причину\
"""

PAYMENT_NOT_CONFIRMED: str = """\
🕘 Оплата ещё не прошла, подождите!\
"""

TARIFF_PAYMENT_CANCELED: str = """\
❌ Оплата отменена!"""

COOPERATION_MESSAGE: str = """\
📑 Уважаемый будущий партнёр
Просьба заполнить данную Google Forms после чего мы свяжемся с вами \
для обсуждения более широкого формата сотрудничества

<b>Google Forms</b>

📊 Так же информация со своей стороны готовы предоставить партнёру 

<b>Презентация</b>\
"""

CONFIDENT_MESSAGE: str = """\
<blockquote>🔒 Конфиденциальность</blockquote>

<b>Политика конфиденциальности Telegram бота SharkVPN</b>
Администрация Telegram бота SharkVPN обязуется сохранять вашу конфиденциальность в \
Интернете. Мы уделяем большое значение охране предоставленных вами данных. Наша \
политика конфиденциальности основана на требованиях политик конфиденциальности \
Telegram и магазинов Apple и Google. 
Мы не собираем и не обрабатываем персональные данные пользователей. \
Наш Telegram бот в целях осуществления работы сервиса использует \
только неперсонализированный Telegram ID.

<b>Сбор и использование персональных данных</b>
Мы не запрашиваем и не собираем никаких персональных данных. Все данные \
пользователей в нашем сервисе привязаны только к неперсонализированному Telegram ID.
Когда вы запускаете Telegram бот SharkVPN Telegram автоматически передает \
нам только ваш Telegram ID, который не дает нам доступа к вашей личной информации.

<b>Хранение данных, изменение и удаление</b>
Пользователь, предоставивший свой Telegram-ID нашему Telegram боту SharkVPN \
имеет право на удаление своих данных, привязанных к Telegram ID, кроме информации о блокировке пользователя.

<b>Раскрытие информации третьим лицам</b>
Мы не продаем, не используем и не раскрываем третьим лицам какие-либо \
данные своих пользователей для каких-либо целей.

<b>Предоставление информации детям</b>
Если вы являетесь родителем или опекуном, и вы знаете, что ваши дети \
предоставили нам свои данные без вашего согласия, свяжитесь с нами. 

<b>Изменения в политике конфиденциальности</b>
Telegram бот SharkVPN может обновлять нашу политику конфиденциальности \
время от времени. Мы сообщаем о любых изменениях, разместив новую политику \
конфиденциальности на этой странице. Если вы оставили данные у нас, то мы \
оповестим вас об изменении в политике конфиденциальности при помощи бота SharkVPN

<b>Обратная связь, заключительные положения</b>
Связаться с администрацией Telegram бота SharkVPN по вопросам, связанным с \
политикой конфиденциальности можно с помощью контактной информации указанной \
в разделе Помощь нашего бота. Если вы не согласны с данной политикой \
конфиденциальности, вы не можете пользоваться услугами Telegram бота SharkVPN\
"""

CONFIG_FILE_NOT_FOUND: str = """\
Файл не найден. Возможно он был удалён из-за окончания срока действия тарифа\
"""

CONFIG_FILE: str = """\
Конфиг: {config_name}
Активен до: {expiring_at}\
"""

CONFIG_OVERDUED: str = """\
Срок действия конфига {config_name} истёк!
Вы можете приобрести новый
"""

REFERAL_MESSAGE: str = """\
<b>Реферальная ссылка другу:</b>

<code>{referal_link}</code>

🤑 После активации VPN вы получите 80₽ на аккаунт, приглашённый 100₽ при регистрации\
"""

BALANCE_MENU: str = """\
<blockquote>💰 Баланс</blockquote>

На Вашем счету: {balance} руб.
   ⊦ Заработано с реферальной системы: {earned} руб.

Вы можете пополнить баланс или вывести средства\
"""

BALANCE_CASH_IN_AMOUNT: str = """\
Введите сумму, на которую хотите пополнить баланс\
"""

BALANCE_CASH_OUT_AMOUNT: str = """\
Введите сумму, которую хотите вывести\
"""

INVALID_AMOUNT: str = """\
Некорректная сумма. Попробуйте ввести только цифру. \
В качестве разделителя целой части и копеек используйте точку или запятую\
"""

BALANCE_CASH_IN_METHOD: str = """\
Сумма: {amount} руб.

Выберите метод пополнения\
"""

BALANCE_CASH_OUT_METHOD: str = """\
Сумма: {amount} руб.

Выберите метод вывода средств\
"""

BALANCE_CASH_IN_USDT: str = """\
❗️Указывайте точную сумму USDT при переводе

USDT (TRC20)
Кошелёк 

Обработка займёт не более 30 минут\
"""

BALANCE_CASH_IN_CARD: str = """\
❗️Указывайте точную сумму при переводе

Альфа-Банк
0000-0000-0000-0000

Обработка займёт не более 30 минут\
"""

BALANCE_CASH_IN_SUCCESS: str = """\
Баланс успешно пополнен!

Ваш текущий баланс: {balance} руб.\
"""

OPERATION_CANCELLED: str = """\
❌ Операция отменена!\
"""

BALANCE_CASH_OUT_USDT: str = """\
Обработка заявки занимает до 24ч
Укажите ваш кошелёк USDT (TRC20)\
"""

BALANCE_CASH_OUT_CARD: str = """\
Обработка заявки занимает до 24ч
Укажите ваш номер карты и банк\
"""

BALANCE_CASH_OUT_CREATED: str = """\
Заявка на вывод средств создана! Ожидайте поступления средств\
"""

FAQ_MENU: str = """\
<blockquote>❓ Помощь 24/7</blockquote>

Здесь Вы можете узнать ответы на популярные вопросы по работе сервиса \
или связаться с нами и описать Вашу проблему\
"""

FAQ_INSTRUCTION: str = """\
- Настроить ВПН просто, давайте мы поможем

1. Скачать приложение активатор OpenVPN
2. Зайти в приложение 
3. Откройте файл который прислал вам Shark bot
4. Кнопка поделиться, выбрать приложение OpenVPN

<blockquote>Готово, ваш ВПН теперь работает через одну кнопку Активировать</blockquote>\
"""

FAQ_SUPPORT: str = """\
⚙️ Мы с радостью окажем вам техническую поддержку

<b>Аккаунт поддержки</b>

❗️Обязательно подпишитесь на наш телеграмм аккаунт, чтобы \
знать про наши акции и тех. работы Телеграмм канал\
"""

FAQ_CASHOUTS: str = """\
⭐️ Выплаты отрабатываются в ручную и занимают до 24ч 
Мы предоставляем вывод двумя способами (Карта РФ или USDT (TRC20))

❗️ Обратите внимание
Минимальная сумма вывода 2.000₽\
"""

FAQ_THEMES: str = """\
<blockquote>❓ Помощь 24/7</blockquote>

Выберите тему\
"""

FAQ_PROBLEMS: str = """\
<blockquote>❓ Помощь 24/7</blockquote>

Выберите проблему\
"""

FAQ_PROBLEM: str = """\
<blockquote>❓ Помощь 24/7</blockquote>

<b>Проблема: {question}</b>

<b>Решение: </b>
{solution}\
"""