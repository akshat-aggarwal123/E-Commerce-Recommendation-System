const RecommendationList = ({ recommendations }) => {
    return (
      <div className="recommendation-grid">
        {recommendations.map((product) => (
          <div key={product.Product_ID} className="product-card">
            <h3>{product.Product_ID}</h3>
            <p>Category: {product.Category}</p>
            <p>Subcategory: {product.Subcategory}</p>
            <p>Price: ${product.Price}</p>
            <p>Brand: {product.Brand}</p>
            <p>Ratings: ⭐{product.Ratings}</p>
            <p>Recommendation Score: {product.Recommendation_Score.toFixed(2)}</p>
          </div>
        ))}
      </div>
    );
  };
  
  export default RecommendationList;