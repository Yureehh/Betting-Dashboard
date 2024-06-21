import streamlit as st


def setup(page_title, page_icon=""):
    """Setup the Streamlit page with the given title and icon."""
    st.set_page_config(
        page_title=page_title,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": "Public ledger of my betting activity.\nTwitter: @Yureehwastaken",
        },
        page_icon=page_icon,
    )

    st.markdown(
        """
        <style>

            html, body, div, span, applet, object, iframe,
            h1, h2, h3, h4, h5, h6, p, blockquote, pre,
            a, abbr, acronym, address, big, cite, code,
            del, dfn, em, img, ins, kbd, q, s, samp,
            small, strike, strong, sub, sup, tt, var,
            b, u, i, center,
            dl, dt, dd, ol, ul, li,
            fieldset, form, label, legend,
            table, caption, tbody, tfoot, thead, tr, th, td,
            article, aside, canvas, details, embed,
            figure, figcaption, footer, header, hgroup,
            menu, nav, output, ruby, section, summary,
            time, mark, audio, video,
            .main .block-container, [class*="css"] {
                font-family: 'Source Code Pro', monospace;
            }

            h1, .main .block-container {
                font-family: 'Source Code Pro', monospace;
            }

            .main .block-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 2rem;
            }
            .stMetric {
                text-align: center;
            }
            .block-container table {
                margin-top: 2rem;
            }
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #f1f1f1;
                text-align: center;
                padding: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title(page_title)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
