START_MESSAGE: str = """\
Привет, <b>{full_name}!</b>

Добро пожаловать в SharkBot. Здесь Вы можете приобрести конфиг VPN\
"""

TARIFFS_MENU: str = """\
<blockquote>💵 Тарифы</blockquote>

Вот список действующих тарифов. Выбирайте понравившийся\
"""

TARIFF_PAYMENT: str = """\
Выбран тариф: {title} - {price} руб.

Проведите оплату в мини-приложении по кнопке «Оплатить»
После оплаты нажмите на кнопку «✅ Готово»\
"""

TARIFF_PAYMENT_DONE: str = """\
✅ Оплата проведена успешно!

Ваш конфиг: {config_name}
Активен до: {expiring_at}\
"""

TARIFF_PAYMENT_CANCELED: str = """\
❌ Оплата отменена!"""

COOPERATION_MESSAGE: str = """\
<blockquote>🤝 Сотрудничество</blockquote>

Коммерческое предложение\
"""

CONFIDENT_MESSAGE: str = """\
<blockquote>🔒 Конфиденциальность</blockquote>

<b>Политика конфиденциальности Telegram бота ........</b>
Администрация Telegram бота ....... обязуется сохранять вашу конфиденциальность в \
Интернете. Мы уделяем большое значение охране предоставленных вами данных. Наша \
политика конфиденциальности основана на требованиях политик конфиденциальности \
Telegram и магазинов Apple и Google. 
Мы не собираем и не обрабатываем персональные данные пользователей. \
Наш Telegram бот в целях осуществления работы сервиса использует \
только неперсонализированный Telegram ID.

<b>Сбор и использование персональных данных</b>
Мы не запрашиваем и не собираем никаких персональных данных. Все данные \
пользователей в нашем сервисе привязаны только к неперсонализированному Telegram ID.
Когда вы запускаете Telegram бот ...... Telegram автоматически передает \
нам только ваш Telegram ID, который не дает нам доступа к вашей личной информации.

<b>Хранение данных, изменение и удаление</b>
Пользователь, предоставивший свой Telegram-ID нашему Telegram боту ...... \
имеет право на удаление своих данных, привязанных к Telegram ID, кроме информации о блокировке пользователя.

<b>Раскрытие информации третьим лицам</b>
Мы не продаем, не используем и не раскрываем третьим лицам какие-либо \
данные своих пользователей для каких-либо целей.

<b>Предоставление информации детям</b>
Если вы являетесь родителем или опекуном, и вы знаете, что ваши дети \
предоставили нам свои данные без вашего согласия, свяжитесь с нами. 

<b>Изменения в политике конфиденциальности</b>
Telegram бот ....... может обновлять нашу политику конфиденциальности \
время от времени. Мы сообщаем о любых изменениях, разместив новую политику \
конфиденциальности на этой странице. Если вы оставили данные у нас, то мы \
оповестим вас об изменении в политике конфиденциальности при помощи бота ......

<b>Обратная связь, заключительные положения</b>
Связаться с администрацией Telegram бота ...... по вопросам, связанным с \
политикой конфиденциальности можно с помощью контактной информации указанной \
в разделе Помощь нашего бота. Если вы не согласны с данной политикой \
конфиденциальности, вы не можете пользоваться услугами Telegram бота ......\
"""

CONFIG_FILE_NOT_FOUND: str = """\
Файл не найден. Возможно он был удалён из-за окончания срока действия тарифа\
"""

CONFIG_FILE: str = """\
Конфиг: {config_name}
Активен до: {expiring_at}\
"""

REFERAL_MESSAGE: str = """\
<blockquote>👥 Реферальная система</blockquote>

Приглашайте пользователей по своей реферальной ссылке и получайте бонусы

🔗 Ваша реферальная ссылка:
<code>{referal_link}</code>

Заработано: {earned} руб.

Приглашено: {referals_count} чел.
{referals}\
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
Внесите средства в количестве: {usdt_amount} USDT на данный кошелёк:
<code>{wallet}</code>

После пополнения нажмите на кнопку «✅ Готово»\
"""

BALANCE_CASH_IN_CARD: str = """\
Проведите оплату в мини-приложении по кнопке «Пополнить»
После пополнения нажмите на кнопку «✅ Готово»\
"""

BALANCE_CASH_IN_SUCCESS: str = """\
Баланс успешно пополнен!

Ваш текущий баланс: {balance} руб.\
"""

OPERATION_CANCELLED: str = """\
❌ Операция отменена!\
"""

BALANCE_CASH_OUT_USDT: str = """\
Сумма: {amount} руб.
Метод: USDT

Введите номер своего USDT-TRC20 кошелька\
"""

BALANCE_CASH_OUT_CARD: str = """\
Сумма: {amount} руб.
Метод: карта

Введите номер своей карты\
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
Инструкция\
"""

FAQ_SUPPORT: str = """\
Тех. поддержка\
"""

FAQ_CASHOUTS: str = """\
Выплаты\
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