import streamlit as st

from commons import HORIZONTAL_LINE, SINGLE_VERTICAL_SPACE, setup

# Constants for Referral Program
REFERRAL_LINK = "https://thunderpick.io?r=ORACLE_BETS"
REFERRAL_CODE = "ORACLE_BETS"
DOUBLE_DEPOSIT_BONUS = "Double your first deposit!"
VIP_BENEFITS = "VIP access on LoL Oracle to exclusive perks!"
REFERRAL_COPY_BUTTON = "Copy Referral Link"
REFERRAL_CODE_BUTTON = "Copy Referral Code"
REFERRAL_BUTTON_TOOLTIP = "Referral code copied to clipboard!"
REFERRAL_BONUS_DESCRIPTION = (
    "Join Thunderpick with my referral link or code and enjoy a double bonus on your first deposit. "
    "Invite your friends to join too and get rewarded with VIP status, giving you access to more bets and exclusive benefits."
)
TITLE_TEXT = "🎉 Welcome to the LoL-Oracle Referral Program!"


def render_expanded_referral_page():
    """
    Renders an expanded referral page with detailed information on how users can benefit from the referral program.
    """
    st.subheader(f"🚀 **{DOUBLE_DEPOSIT_BONUS}**")
    st.write(
        "When you sign up using the link or code below, Thunderpick will double your first deposit."
    )
    st.write(
        "This means you can start betting with twice the amount you deposit, giving you more chances to win big!"
    )
    st.markdown(SINGLE_VERTICAL_SPACE, unsafe_allow_html=True)

    st.markdown(HORIZONTAL_LINE, unsafe_allow_html=True)

    st.subheader("🔥 Spread the Word and Get Rewarded:")
    st.write(
        f"Invite others to join Thunderpick using this referral link or code, and you'll gain **{VIP_BENEFITS}**."
    )
    st.write(
        "As a VIP, you'll enjoy enhanced betting options, exclusive tips, and even more rewards tailored just for you."
    )

    st.markdown(HORIZONTAL_LINE, unsafe_allow_html=True)

    st.subheader("📢 How to Get Started:")
    st.write(
        "1. **Join Thunderpick:** Use the referral link or code provided above to create your account and make your first deposit."
    )
    st.write(
        f"2. **Get {DOUBLE_DEPOSIT_BONUS}:** Enjoy the boost to your first deposit, doubling your starting balance."
    )
    st.write(
        f"3. **Refer Friends:** Share this referral link or code with others. When they join, you'll gain **{VIP_BENEFITS}**."
    )
    st.write(
        "4. **Enjoy VIP Perks:** With VIP status, unlock access to exclusive bets, tips, and more rewards as part of our community."
    )


def main():
    """
    Main function to set up the page and render the expanded referral content.
    """
    setup(TITLE_TEXT)
    render_expanded_referral_page()


if __name__ == "__main__":
    main()
