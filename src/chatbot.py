import openai

from data import api_keys

prompt = "with Yes No only - does the text contain any resolution or suggestion that might affect lgbtq people? "


def ask_if_affects_lgbt(text):
    openai.api_key = api_keys.openai_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user",
             "content": "with Yes No only - does the text contain any resolution or suggestion that might affect lgbtq people? Start your answer with yes or no."
                        +
                        text

             },
        ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    # print(result)
    return result

if __name__ == "__main__":
    # text = '''
    # אני רוצה להפנות את הדברים שלי לחבר הכנסת נתניהו, ראש הממשלה המיועד. חבר הכנסת נתניהו, מאוד קל לומר באנגלית לתקשורת הזרה שאתה תומך בקהילת הלהט"ב. מאוד קל לתדרך מאחורי הקלעים את העיתונאים שאין מה לחשוש, שלא תהיה שום פגיעה בזכויות של קהילת הלהט"ב. אבל בוא, בוא נשמע אותך אומר את הדברים מעל בימה הזו, לנו וגם לשותפים שלך. בוא ותגיד את הדברים גם לשותפים ההומופובים שלך אבי מעוז, בצלאל סמוטריץ' ואורית סטרוק. בוא נשמע את כל ההבטחות האלה כאן בכנסת בעברית פשוטה וברורה. יותר מכך – בוא נראה מעשים.
    #     '''
    text = '''
    הצעת חוק האזרחים הוותיקים (תיקון – חניה חינם לאזרח ותיק שמלאו לו 75 שנים), התשפ"ג–2023, מאת חברי הכנסת יונתן מישרקי, יצחק קרויזר וארז מלול; הצעת חוק סיוע לצעירים חסרי עורף משפחתי, התשפ"ג–2023, מאת חברת הכנסת קארין אלהרר; הצעת חוק פיצויי פיטורים (תיקון – התפטרות בשל השתתפות במכינה קדם צבאית), התשפ"ג–2023, מאת חבר הכנסת רון כץ. תודה.
    '''
    ask_if_affects_lgbt(text)
