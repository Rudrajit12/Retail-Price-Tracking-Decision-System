import pandas as pd

def run_comparison():
    print("Running Reliance Digital price comparison...")

    df = pd.read_csv("price_log.csv")

    # -------------------------------
    # PRICE PIVOT
    # -------------------------------
    price_pivot = df.pivot_table(
        index=["product_id", "product_name"],
        columns="site",
        values="price",
        aggfunc="first"
    ).reset_index()

    print("\n Pivot columns:", price_pivot.columns.tolist())

    # Ensure all expected columns exist
    for col in ["Reliance Digital", "Amazon", "Flipkart"]:
        if col not in price_pivot.columns:
            price_pivot[col] = pd.NA

    price_pivot = price_pivot.rename(columns={
        "Reliance Digital": "reliance_price",
        "Amazon": "amazon_price",
        "Flipkart": "flipkart_price",
    })

    # Convert to numeric
    for col in ["reliance_price", "amazon_price", "flipkart_price"]:
        if col in price_pivot.columns:
            price_pivot[col] = pd.to_numeric(price_pivot[col], errors="coerce")

    # -------------------------------
    # MARKET REFERENCE PRICE
    # -------------------------------
    price_pivot["market_min_price"] = price_pivot[
        ["amazon_price", "flipkart_price"]
    ].min(axis=1, skipna=True)

    # -------------------------------
    # PRICE GAP CALCULATIONS
    # -------------------------------
    price_pivot["price_gap"] = (
        price_pivot["reliance_price"] - price_pivot["market_min_price"]
    )

    price_pivot["gap_percent"] = (
        (price_pivot["price_gap"] / price_pivot["market_min_price"]) * 100
    ).round(2)

    # -------------------------------
    # PRICING POSITION
    # -------------------------------
    def pricing_position(row):
        if row["gap_percent"] > 5:
            return "Overpriced vs Market"
        elif row["gap_percent"] < -5:
            return "Underpriced vs Market"
        else:
            return "Competitive"

    price_pivot["pricing_position"] = price_pivot.apply(pricing_position, axis=1)

    # -------------------------------
    # ACTION RECOMMENDATION
    # -------------------------------
    def pricing_action(row):
        if row["gap_percent"] > 5:
            return "Decrease Reliance Price"
        elif row["gap_percent"] < -5:
            return "Increase Reliance Price"
        else:
            return "Maintain Reliance Price"

    price_pivot["action_recommended"] = price_pivot.apply(pricing_action, axis=1)

    # -------------------------------
    # STOCK PIVOT
    # -------------------------------
    stock_pivot = df.pivot_table(
        index=["product_id", "product_name"],
        columns="site",
        values="stock",
        aggfunc="first"
    ).reset_index()

    stock_pivot = stock_pivot.rename(columns={
        "Reliance Digital": "reliance_stock_status",
        "Amazon": "amazon_stock_status",
        "Flipkart": "flipkart_stock_status",
    })

    final = price_pivot.merge(
        stock_pivot,
        on=["product_id", "product_name"],
        how="left"
    )

    # -------------------------------
    # STOCK-LED OPPORTUNITY
    # -------------------------------
    def stock_opportunity(row):
        reliance_stock = str(row["reliance_stock_status"]).lower()
        amazon_stock = str(row["amazon_stock_status"]).lower()
        flipkart_stock = str(row["flipkart_stock_status"]).lower()

        if (
            "In Stock" in reliance_stock and
            "Out of Stock" in amazon_stock and
            "Out of Stock" in flipkart_stock
        ):
            return "Increase Reliance Price (all competitors OOS)"

        if (
            "In Stock" in reliance_stock and
            "Out of Stock" in amazon_stock
        ):
            return "Increase Reliance Price (Amazon OOS)"

        if (
            "In Stock" in reliance_stock and
            "Out of Stock" in flipkart_stock
        ):
            return "Increase Reliance Price (Flipkart OOS)"

        return "No stock-based opportunity"

    final["stock_opportunity"] = final.apply(stock_opportunity, axis=1)

    # -------------------------------
    # SAVE OUTPUT
    # -------------------------------
    final.to_csv("price_comparison_results.csv", index=False)

    print("Reliance Digital comparison complete!\n")
    print("Saved to price_comparison_results.csv\n")
