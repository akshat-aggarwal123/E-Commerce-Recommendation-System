import React from 'react';
import './RecommendationList.css'; // Create this file for styling

const RecommendationList = ({ recommendations, aiInsights = null, isLoading = false }) => {
  return (
    <div className="recommendations-container">
      {/* AI Insights Section */}
      {aiInsights && (
        <div className="ai-insights">
          <h2>AI-Powered Insights</h2>
          <div className="insight-content">
            {aiInsights}
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading ? (
        <div className="loading-indicator">Loading recommendations...</div>
      ) : (
        /* Product Recommendations Grid */
        <div className="recommendation-section">
          <h2>Recommended Products</h2>
          <div className="recommendation-grid">
            {recommendations && recommendations.length > 0 ? (
              recommendations.map((product) => (
                <div key={product.Product_ID} className="product-card">
                  <h3>{product.Product_ID}</h3>
                  <p>Category: {product.Category}</p>
                  <p>Subcategory: {product.Subcategory}</p>
                  <p>Price: ${product.Price}</p>
                  <p>Brand: {product.Brand}</p>
                  <p>Ratings: ⭐{product.Ratings}</p>
                  <p>Recommendation Score: {product.Recommendation_Score.toFixed(2)}</p>
                </div>
              ))
            ) : (
              <p className="no-recommendations">No recommendations available</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default RecommendationList;
