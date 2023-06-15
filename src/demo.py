import streamlit as st
from scraping.tools import scrape_aspx
from common import URLS, KEYWORDS
from chatbot import ask_if_affects_lgbt


scrape_url = None
search_kw = False
gpt = False


def choose_url_to_scrape():
    form_name = "url_form"
    url = st.sidebar.selectbox(
        "בחרו אתר לחיפוש טקסטים",
        ("choose option", "knesset", "gov.il", "load PDF/DOCX", "other URL")
    )
    if url != "choose option":
            if url in ["load PDF/DOCX", "other URL"]:
                url = st.text_input('insert url...')
            scrape_url = st.form_submit_button("Submit")
    return form_name, url, scrape_url


with st.sidebar:
    with st.form("url_form"):
        url = st.sidebar.selectbox(
            "בחרו אתר לחיפוש טקסטים",
            ("choose option", "knesset", "gov.il", "load PDF/DOCX", "other URL")
        )
        if url != "choose option":
                if url in ["load PDF/DOCX", "other URL"]:
                    st.write('insert url...')
                    url = st.text_input('insert url...')
                scrape_url = st.form_submit_button("Submit")

    with st.form("text_form"):
        text_input = st.text_area('הכניסו טקסט')

        submitted_text = st.form_submit_button("search keywords")
        submit_to_gpt = st.form_submit_button("is this text offensive? ask ChatGPT   ")
        if submitted_text:
            search_kw = True
        if submit_to_gpt:
            gpt = True


def is_relevant(text, kwords):
    paragraphs = text.split("\n")
    for paragraph in paragraphs:
        text_to_print = ""
        is_para_relevant = False
        for sentence in paragraph.split('. '):
            if any(k in sentence for k in kwords):
                text_to_print += f"<b>{sentence}</b>. "
                is_para_relevant = True
            else:
                text_to_print += sentence + ". "

        if is_para_relevant:
            st.write(f'this text contains lgbtq relevant text: ')
            st.markdown(text_to_print + "\n", unsafe_allow_html=True)


# @st.cache
async def get_scraped_links(url):
    list_of_urls = await scrape_aspx(url)
    return list_of_urls


def main():
    st.title('זיהוי נושאים להטבים בהחלטות ממשלה')
    if scrape_url:
        if url == "knesset":
            hakika_url = URLS['hakika']
            urls = get_scraped_links(hakika_url)
            print(urls)
            st.write(urls)
    if text_input:
        if search_kw:
            # keywords = parse_key_words().split("\n")
            is_relevant(text_input, KEYWORDS)
        elif gpt:
            st.write(text_input[:200] +"...")
            st.markdown("**האם יש בטקסט זה כדי להשפיע על הקהילה הגאה?**")
            is_offensive = ask_if_affects_lgbt(text_input[:4000])
            print(is_offensive)
            st.write(is_offensive)


if __name__ == '__main__':
    model_name = "google/mt5-small"
    # model_name = "csebuetnlp/mT5_multilingual_XLSum"
    main()