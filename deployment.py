import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import plotly.express as px
from datetime import date

# Database connection configuration
def connect_to_db():
    
    # Supabase credentials (adjust with your actual password)
    user = st.secrets["postgres"]["user"]
    password = st.secrets["postgres"]["password"]
    host = st.secrets["postgres"]["host"]  # Usar el host externo
    port = st.secrets["postgres"]["port"]
    database = st.secrets["postgres"]["database"]

    #'''TEXTO DE PRUEBA - NO DEBE VERSE'''

    
    # Crear la cadena de conexión sin pool_mode y con sslmode=require
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url)
    
   

    return engine

# Load data from the database based on selected date range
def load_data(engine, start_date, end_date):
    # Only select products with discount_amount > 0 to focus on those with promotions
    query = f"""
    SELECT *
    FROM productos_amazon
    WHERE date >= '{start_date}' AND date <= '{end_date}' AND discount_amount > 0;
    """
    df = pd.read_sql(query, engine)
    return df

def main():
    st.title(":blue[Discount Analysis Dashboard]: :orange[Amazon]")

    st.sidebar.header("Settings")

    # Database Connection
    st.sidebar.subheader("Database Connection")
    engine = connect_to_db()
    st.sidebar.success("Connected to the database")

    # Date Filters
    st.sidebar.header("Filters")
    default_start = date(2024, 11, 14)  # One day before Buen Fin
    default_end = date(2024, 12, 19)     # 10 days after Buen Fin
    start_date = st.sidebar.date_input("Start Date", value=default_start)
    end_date = st.sidebar.date_input("End Date", value=default_end)

    # Load and display data
    st.sidebar.subheader("Data Loading")
    df = load_data(engine, start_date, end_date)
    st.sidebar.success("Data loaded successfully!")

    if df.empty:
        st.error("No data available for the selected filters.")
        return

    # Additional filter by product type
    product_types_list = st.sidebar.multiselect(
        "Select Product Type(s)",
        options=df["product_type"].unique(),
        default=df["product_type"].unique().tolist()
    )
    df = df[df["product_type"].isin(product_types_list)]

    if df.empty:
        st.error("No data available for the selected product types.")
        return

    # Key Metrics (KPIs)
    st.subheader(":red[Key Metrics]")
    col1, col2, col3 = st.columns(3)
    total_products = len(df)
    avg_discount = df["discount_percentage"].mean()
    avg_rating = df["rating"].mean()

    col1.metric("Products with Discounts", total_products)
    col2.metric("Average Discount (%)", f"{avg_discount:.2f}%")
    col3.metric("Average Rating", f"{avg_rating:.2f}")

    # General Insights
    st.markdown("""
    **Initial Insights:**
    - A higher number of discounted products may indicate more aggressive promotional strategies.
    - A high average discount suggests attractive offers, especially during peak events like Buen Fin.
    - A high average rating, even with discounts, suggests that quality or customer satisfaction is not compromised.
    - As time progresses (days, weeks, months), these metrics can change, reflecting market shifts, seasonal effects, or evolving customer preferences.
    """)

    # Tabs for different types of visualizations
    tab1, tab2, tab3 = st.tabs(["Trends", "Distributions", "Comparisons"])

    # -------------------- TAB 1: Trends --------------------
    with tab1:
        st.write("### Time-based Trends")

        # Average discount by product type over time
        avg_discount_by_pt = df.groupby(["date", "product_type"])["discount_percentage"].mean().reset_index()
        fig_avg_discount = px.line(
            avg_discount_by_pt,
            x="date",
            y="discount_percentage",
            color="product_type",
            title="Average Discount by Product Type",
            labels={"discount_percentage": "Discount (%)", "date": "Date"}
        )
        st.plotly_chart(fig_avg_discount)

        st.markdown("""
        **Insight:**  
        Observe how discounts may spike around key dates (e.g., the start of Buen Fin) and then diminish.  
        Over longer periods (weeks or months), you might detect seasonal trends or recurring promotional patterns.
        """)

        # Average reviews by product type
        avg_reviews_by_pt = df.groupby(["date", "product_type"])["reviews_count"].mean().reset_index()
        fig_avg_reviews = px.line(
            avg_reviews_by_pt,
            x="date",
            y="reviews_count",
            color="product_type",
            title="Average Reviews by Product Type",
            labels={"reviews_count": "Average Reviews", "date": "Date"}
        )
        st.plotly_chart(fig_avg_reviews)

        st.markdown("""
        **Insight:**  
        An increase in the average number of reviews might indicate growing interest, potentially driven by discounts or promotional periods.  
        Over time, you can correlate spikes in reviews with promotional events.
        """)

        # Average rating by product type
        avg_rating_by_pt = df.groupby(["date", "product_type"])["rating"].mean().reset_index()
        fig_avg_rating = px.line(
            avg_rating_by_pt,
            x="date",
            y="rating",
            color="product_type",
            title="Average Rating by Product Type",
            labels={"rating": "Average Rating", "date": "Date"}
        )
        st.plotly_chart(fig_avg_rating)

        st.markdown("""
        **Insight:**  
        A constant or rising average rating during discount periods suggests that offers do not compromise product quality or satisfaction.
        """)

        # Number of products with Buen Fin discount over time
        buen_fin_counts = df[df["buen_fin_discount"] > 0].groupby(["date", "product_type"])["name"].count().reset_index()
        buen_fin_counts.rename(columns={"name": "count"}, inplace=True)
        fig_buen_fin_counts = px.line(
            buen_fin_counts,
            x="date",
            y="count",
            color="product_type",
            title="Number of Products with Buen Fin Discount",
            labels={"count": "Number of Products", "date": "Date"}
        )
        st.plotly_chart(fig_buen_fin_counts)

        st.markdown("""
        **Insight:**  
        It's expected to see a spike in discounted products during Buen Fin.  
        After this event, observe whether the number returns to lower levels or if a residual promotional effect lingers.
        """)

        # Comparison of General, Buen Fin, and Black Friday discounts
        st.write("### Comparison of Discounts: General, Buen Fin, and Black Friday")
        discounted_products = df[df["has_discount"] == True]
        base = discounted_products[["date", "product_type"]].drop_duplicates()

        # Counts for each discount type
        general_discounts = discounted_products.groupby(["date", "product_type"])["has_discount"].sum().reset_index()
        general_discounts.rename(columns={"has_discount": "count"}, inplace=True)
        general_discounts["discount_type"] = "General"

        buen_fin_dis = discounted_products.groupby(["date", "product_type"])["buen_fin_discount"].sum().reset_index()
        buen_fin_dis.rename(columns={"buen_fin_discount": "count"}, inplace=True)
        buen_fin_dis["discount_type"] = "Buen Fin"

        black_friday_dis = discounted_products.groupby(["date", "product_type"])["black_friday_discount"].sum().reset_index()
        black_friday_dis.rename(columns={"black_friday_discount": "count"}, inplace=True)
        black_friday_dis["discount_type"] = "Black Friday"

        general_discounts = pd.merge(base, general_discounts, how="left", on=["date", "product_type"]).fillna(0)
        buen_fin_dis = pd.merge(base, buen_fin_dis, how="left", on=["date", "product_type"]).fillna(0)
        black_friday_dis = pd.merge(base, black_friday_dis, how="left", on=["date", "product_type"]).fillna(0)

        discount_counts = pd.concat([general_discounts, buen_fin_dis, black_friday_dis])
        fig_discount_comparison = px.bar(
            discount_counts,
            x="date",
            y="count",
            color="discount_type",
            barmode="stack",
            facet_col="product_type",
            title="Comparison of Discounts: General, Buen Fin and Black Friday by Product Type",
            labels={
                "product_type": "",
                "count": "Number of Discounts",
                "date": "",
                "discount_type": "Discount Type"
            },
            color_discrete_map={"General": "blue", "Buen Fin": "green", "Black Friday": "orange"}
        )

        # Remove "product_type=" from facet annotations
        for annotation in fig_discount_comparison.layout.annotations:
            if "=" in annotation.text:
                annotation.text = annotation.text.split("=")[-1]

        st.plotly_chart(fig_discount_comparison)

        st.markdown("""
        **Insight:**  
        This view helps you understand which discount type is dominant over time.  
        For example, during Buen Fin, the green bar should rise significantly. Later, if Black Friday occurs, the orange bar may appear.  
        Comparing these events over longer periods can reveal which promotions are more effective.
        """)

        # If too many product types, split into multiple charts
        product_types = df["product_type"].unique()
        if len(product_types) > 3:
            st.write("### Separate Charts for Product Groups")
            grouped_product_types = [product_types[i:i + 3] for i in range(0, len(product_types), 3)]
            titles = [f"Chart {idx+1}: Products (Group {idx+1})" for idx in range(len(grouped_product_types))]

            for idx, group in enumerate(grouped_product_types):
                group_data = discount_counts[discount_counts["product_type"].isin(group)]
                fig_discount_comparison_group = px.bar(
                    group_data,
                    x="date",
                    y="count",
                    color="discount_type",
                    barmode="stack",
                    facet_col="product_type",
                    title=titles[idx],
                    labels={
                        "product_type": "Product Type",
                        "count": "Number of Discounts",
                        "date": "Date",
                        "discount_type": "Discount Type"
                    },
                    color_discrete_map={"General": "blue", "Buen Fin": "green", "Black Friday": "orange"}
                )

                # Remove "product_type=" from facet annotations in group charts
                for annotation in fig_discount_comparison_group.layout.annotations:
                    if "=" in annotation.text:
                        annotation.text = annotation.text.split("=")[-1]
                st.plotly_chart(fig_discount_comparison_group)

            st.markdown("""
            **Insight:**  
            By dividing product types into groups, you can focus on fewer categories without overcrowding.  
            Over time, as more product types appear in the database, this approach helps maintain clarity and accessibility of the insights.
            """)

    # -------------------- TAB 2: Distributions --------------------
    with tab2:
        st.write("### Data Distributions")

        # Boxplot of discounts by product type
        st.subheader("Distribution of Discounts by Product Type")
        fig_box = px.box(
            df,
            x="product_type",
            y="discount_percentage",
            title="Discount Distribution",
            labels={"product_type": "Product Type", "discount_percentage": "Discount (%)"}
        )
        st.plotly_chart(fig_box)

        st.markdown("""
        **Insight:**  
        A boxplot reveals median, interquartile ranges, and potential outliers.  
        If some products offer significantly higher discounts than others, they will appear as outliers.  
        Over longer timeframes, watch if distributions become more uniform (fewer outliers) or more dispersed.
        """)

        # Histogram of rating
        st.subheader("Rating Distribution")
        fig_hist = px.histogram(
            df,
            x="rating",
            nbins=20,
            title="Rating Distribution",
            labels={"rating": "Rating"}
        )
        st.plotly_chart(fig_hist)

        st.markdown("""
        **Insight:**  
        If the rating distribution clusters at high values, it suggests most products are well-received.  
        Over time, shifts in this distribution might indicate improving customer satisfaction or, conversely, declining product quality.
        """)

    # -------------------- TAB 3: Comparisons --------------------
    with tab3:
        st.write("### Comparisons and Correlations")

        # Scatter plot: Discount vs Rating
        st.subheader("Relationship between Discount and Rating")
        fig_scatter = px.scatter(
            df,
            x="discount_percentage",
            y="rating",
            color="product_type",
            title="Discount vs. Rating by Product Type",
            labels={"discount_percentage": "Discount (%)", "rating": "Rating"}
        )
        st.plotly_chart(fig_scatter)

        st.markdown("""
        **Insight:**  
        This plot shows whether there's a correlation between higher discounts and better ratings.  
        Over time, patterns may emerge:  
        - If higher discounts correlate with higher ratings, customers might value bargains highly.  
        - If high discounts do not improve ratings, price might not be the main driver of satisfaction.  
        
        Monitoring this continuously can help adjust long-term discount strategies.
        """)

if __name__ == "__main__":
    main()
