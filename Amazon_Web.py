#import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Custom Dark Blue Theme
# -----------------------------
page_bg = """
<style>
/* Main background */
[data-testid="stAppViewContainer"] {
    background-color: #0d1b2a;  /* Deep dark blue */
    color: white;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #1b263b;  /* Slightly lighter navy */
    color: white;
}

/* Header (remove background bar) */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Make text white in sidebar */
[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)


# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_amazon_data.csv")  
    return df

df = load_data()

st.title("📦 Amazon Sales Data")

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to section:",
    ["📂 Categories", "🛍️ Products", "ℹ️ About Data"],
    index=0  # default = Categories
)

# =============================
# Categories Section
# =============================
if page == "📂 Categories":
    with st.container():
        st.header("📂 Main Categories")

        # 1. Top Categories by Rating
        total_ratings_by_category = df.groupby('main_category')['rating'].sum().sort_values(ascending=False)

        st.subheader("Top Categories by Total Rating")
        top_n_rating = st.slider("Number of categories to show ", 1, 9, 5, key="rating_slider")

        ratings_df = (
            total_ratings_by_category
            .head(top_n_rating)
            .reset_index()
        )

        fig1 = px.bar(
            ratings_df,
            x="main_category",
            y="rating",
            orientation="v",
            color="rating",
            color_continuous_scale="blues",
            title=f"Top {top_n_rating} Categories by Total Ratings"
        )
        fig1.update_layout(
        plot_bgcolor="#0d1b2a",   
        paper_bgcolor="#0d1b2a",  
        font=dict(color="white")  
        )
        st.plotly_chart(fig1, use_container_width=True)

        # 2. Top Categories by Discount
        st.subheader("Top Categories by Average Discount %")
        top_n_discount = st.slider("Number of categories to show ", 1, 9, 5, key="discount_slider")

        avg_discount = (
            df.groupby('main_category')['discount_percentage']
            .mean()
            .sort_values(ascending=False)
            .head(top_n_discount)
            .reset_index()
        )

        fig2 = px.bar(
            avg_discount,
            x="discount_percentage",
            y="main_category",
            orientation="h",
            color="discount_percentage",
            color_continuous_scale="blues",
            title=f"Top {top_n_discount} Categories by Average Discount %"
        )
        fig2.update_layout(
        plot_bgcolor="#0d1b2a",  
        paper_bgcolor="#0d1b2a",  
        font=dict(color="white") 
        )
        st.plotly_chart(fig2, use_container_width=True)


# =============================
# Products Section
# =============================
elif page == "🛍️ Products":
    with st.container():
        st.header("🛍️ Products")

        # Always show top 5 products (no slider)
        top_products = df[['product_name','rating_count']].sort_values(
            by="rating_count", ascending=False
        ).head(6)

        st.subheader("Top 5 Most Reviewed Products")

        fig = px.pie(
            top_products,
            values="rating_count",
            names="product_name",
            title="Top 5 Most Reviewed Products",
            hole=0.3
        )
        fig.update_layout(
        plot_bgcolor="#0d1b2a",  
        paper_bgcolor="#0d1b2a",  
        font=dict(color="white")  
        )
        st.plotly_chart(fig, use_container_width=True)

    
# =============================
# About Data Section
# =============================
elif page == "ℹ️ About Data":
    with st.container():
        st.header("ℹ️ About Data")

        # 1. Price vs Rating
        st.subheader("Relationship Between Product Price and Rating")
        fig2 = px.scatter(
            df, 
            x="actual_price", 
            y="rating", 
            color="rating",
            color_continuous_scale="viridis",
            title="Relationship Between Product Price and Rating"
        )
        fig2.update_layout(
        plot_bgcolor="#0d1b2a",  
        paper_bgcolor="#0d1b2a",  
        font=dict(color="white")  
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.info("📌 Ratings don’t strongly increase with price. There is no clear correlation between higher price and better rating.")

        # 2. Discounts vs Ratings
        st.subheader("Do Bigger Discounts Lead to Higher Ratings?")
        fig3 = px.scatter(
            df,
            x="discount_percentage",
            y="rating",
            color="discount_percentage",
            color_continuous_scale="plasma",
            title="Discount Percentage vs Rating"
        )
        fig3.update_layout(
        plot_bgcolor="#0d1b2a",
        paper_bgcolor="#0d1b2a",  
        font=dict(color="white")  
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.info("📌 Discounts don’t affect rating much.")

        # 3. Discounted Price vs Ratings
        st.subheader("Do Discounted Prices Lead to Higher Ratings?")
        fig4 = px.scatter(
            df,
            x="discounted_price",
            y="rating",
            color="discounted_price",
            color_continuous_scale="magma",
            title="Discounted Price vs Rating"
        )
        fig4.update_layout(
        plot_bgcolor="#0d1b2a",   
        paper_bgcolor="#0d1b2a",  
        font=dict(color="white")  
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.info("📌 Discounted price doesn’t affect rating much — and neither do discount percentage or actual price.")
