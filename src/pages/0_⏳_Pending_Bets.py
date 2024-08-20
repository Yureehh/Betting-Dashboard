import streamlit as st

from commons import VERTICAL_SPACE, load_bets, setup
from sidebar import render_sidebar


def render_pending_bets_df(pending_bets_df):
    """
    Display the pending bets in a DataFrame.

    Args:
        pending_bets_df (pd.DataFrame): The DataFrame containing the pending bets.
    """
    if pending_bets_df.empty:
        st.write("No pending bets to display.")
        return

    st.write("### Pending Bets")
    pending_bets_df["Date"] = pending_bets_df["Date"].dt.date
    pending_bets_df = pending_bets_df.sort_values(by="Date", ascending=False)
    st.dataframe(pending_bets_df, hide_index=True)
    st.markdown(VERTICAL_SPACE, unsafe_allow_html=True)


def main():
    """
    Main function to set up the page and render the pending bets.
    """
    setup("Lol-Oracle Pending Bets")

    all_bets_df = load_bets(pending=True)

    if all_bets_df.empty:
        st.error("No pending bets listed at the moment.")
        return

    filtered_bets_df = render_sidebar(all_bets_df, pending=True)

    render_pending_bets_df(filtered_bets_df)

    st.markdown("<hr>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
