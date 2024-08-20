import streamlit as st

from commons import HORIZONTAL_LINE, setup


def render_referral_page():
    """
    Renders the referral page with a focus on key benefits and a clear call-to-action.
    """
    st.title("🎉 Earn More with LoL-Oracle!")

    st.subheader("Get Your Bonus:")
    st.write("🚀 **Double your first deposit** when you sign up through this link!")

    st.markdown("### 🔗 **Your Referral Link:**")
    referral_link = "https://thunderpick.io?r=ORACLE_BETS"
    st.write(f"[Copy and Share This Link]({referral_link})")

    if st.button("Copy Referral Link"):
        # Placeholder for actual clipboard functionality
        st.write("Referral link copied to clipboard!")

    st.markdown("### 🔥 Spread the Word:")
    st.write("Invite others and get **VIP access** to exclusive bets!")

    st.markdown(HORIZONTAL_LINE, unsafe_allow_html=True)


def main():
    """
    Main function to set up the page and render the referral content.
    """
    setup("LoL-Oracle Referral Program")
    render_referral_page()


if __name__ == "__main__":
    main()
