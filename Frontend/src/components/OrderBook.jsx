import React, { useEffect, useState, useRef } from "react";
import styles from "../styles/OrderBook.module.css";

const OrderBook = ({ symbol = "btcusdt", currentPrice, theme = "dark" }) => {
  const [bids, setBids] = useState([]);
  const [asks, setAsks] = useState([]);
  const [spread, setSpread] = useState(0);
  const wsRef = useRef(null);

  useEffect(() => {
    if (!symbol) return;

    if (wsRef.current) wsRef.current.close();

    wsRef.current = new WebSocket(
      `wss://stream.binance.com:9443/ws/${symbol.toLowerCase()}@depth20@100ms`
    );

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.bids && data.asks) {
          const topBids = data.bids.slice(0, 15).map(([price, qty]) => ({
            price: parseFloat(price),
            quantity: parseFloat(qty),
            total: parseFloat(price) * parseFloat(qty),
          }));

          const topAsks = data.asks.slice(0, 15).map(([price, qty]) => ({
            price: parseFloat(price),
            quantity: parseFloat(qty),
            total: parseFloat(price) * parseFloat(qty),
          }));

          setBids(topBids);
          setAsks(topAsks);

          if (topBids.length > 0 && topAsks.length > 0) {
            const spreadValue = topAsks[0].price - topBids[0].price;
            const spreadPercent = (spreadValue / topBids[0].price) * 100;
            setSpread(spreadPercent);
          }
        }
      } catch (error) {
        console.error("Error parsing order book data:", error);
      }
    };

    wsRef.current.onerror = (err) =>
      console.error("Order Book WebSocket error:", err);

    wsRef.current.onclose = () => console.log("Order Book WebSocket closed");

    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, [symbol]);

  const formatPrice = (price) => {
    if (price >= 1000) return price.toFixed(2);
    if (price >= 1) return price.toFixed(4);
    return price.toFixed(8);
  };

  const formatQuantity = (qty) => {
    if (qty >= 1000) return qty.toFixed(2);
    if (qty >= 1) return qty.toFixed(4);
    return qty.toFixed(8);
  };

  // Pick theme class
  const themeClass =
    theme === "dark" ? styles.orderBookDark : styles.orderBookLight;

  return (
    <div className={`${styles.orderBookContainer} ${themeClass}`}>
      <div className={styles.header}>
        <h3 className={styles.headerTitle}>
          {symbol.toUpperCase()} Order Book
        </h3>
        <div className={styles.headerRow}>
          <span>Price ({symbol.slice(-4).toUpperCase()})</span>
          <span>Amount ({symbol.slice(0, -4).toUpperCase()})</span>
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.asks}>
          {asks.map((ask, idx) => {
            const highlight =
              currentPrice &&
              Math.abs(ask.price - currentPrice) / currentPrice < 0.001;
            return (
              <div
                key={idx}
                className={`${styles.orderRow} ${
                  highlight ? styles.highlightAsk : ""
                }`}
              >
                <span className={styles.orderPriceAsk}>
                  {formatPrice(ask.price)}
                </span>
                <span className={styles.orderQty}>
                  {formatQuantity(ask.quantity)}
                </span>
              </div>
            );
          })}
        </div>

        <div
          className={`${styles.currentPriceSection} ${
            theme === "dark"
              ? styles.currentPriceSectionDark
              : styles.currentPriceSectionLight
          }`}
        >
          {currentPrice && (
            <div
              className={`${styles.currentPrice} ${
                theme === "dark"
                  ? styles.currentPriceDark
                  : styles.currentPriceLight
              }`}
            >
              ${formatPrice(currentPrice)}
            </div>
          )}
          {spread > 0 && (
            <div
              className={`${styles.spread} ${
                theme === "dark" ? styles.spreadDark : styles.spreadLight
              }`}
            >
              Spread: {spread.toFixed(4)}%
            </div>
          )}
        </div>

        <div className={styles.bids}>
          {bids.map((bid, idx) => {
            const highlight =
              currentPrice &&
              Math.abs(bid.price - currentPrice) / currentPrice < 0.001;
            return (
              <div
                key={idx}
                className={`${styles.orderRow} ${
                  highlight ? styles.highlightBid : ""
                }`}
              >
                <span className={styles.orderPriceBid}>
                  {formatPrice(bid.price)}
                </span>
                <span className={styles.orderQty}>
                  {formatQuantity(bid.quantity)}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      <div className={styles.footer}>
        <span>Bids: {bids.length}</span>
        <span>Asks: {asks.length}</span>
      </div>
    </div>
  );
};

export default OrderBook;
