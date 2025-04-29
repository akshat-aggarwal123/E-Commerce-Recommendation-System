// src/components/RecommendationCard.jsx
import React from 'react';
import './RecommendationCard.css';

const RecommendationCard = ({ recommendations, aiInsights, isLoading }) => {
  if (isLoading) {
    return (
      <div className="recommendation-container">
        <div className="loading-card">
          <div className="loading-spinner"></div>
          <p>Finding the best products for you...</p>
        </div>
      </div>
    );
  }

  if (!recommendations || recommendations.length === 0) {
    return null;
  }

  return (
    <div className="recommendation-container">
      {/* AI Insights Header */}
      {aiInsights && (
        <div className="recommendations-header">
          <h2>Recommendations</h2>
          <p className="insights-text">{aiInsights}</p>
        </div>
      )}

      {/* Product Cards */}
      <div className="recommendation-grid">
        {recommendations.map((product) => {
          // Calculate match percentage (for UI purposes, similar to the image)
          const matchPercentage = Math.round(product.Recommendation_Score);

          return (
            <div key={product.Product_ID} className="product-card">
              <div className="product-card-header">
                <h3>{product.Brand}</h3>
                <span className="match-percentage">{matchPercentage}% Match</span>
              </div>

              <div className="product-details">
                <p className="product-description">{product.Description || `${product.Brand} ${product.Category} in ${product.Subcategory}`}</p>

                <div className="product-metrics">
                  <span className="difficulty-level">
                    {product.Ratings >= 4.5 ? 'Premium' :
                     product.Ratings >= 3.5 ? 'Quality' : 'Standard'}
                  </span>
                  <span className="frequency">Price: ${product.Price}</span>
                </div>

                <div className="product-rating">
                  {[...Array(Math.round(product.Ratings))].map((_, i) => (
                    <span key={i} className="star-filled">★</span>
                  ))}
                  {[...Array(5 - Math.round(product.Ratings))].map((_, i) => (
                    <span key={i} className="star-empty">☆</span>
                  ))}
                </div>
              </div>

              <div className="product-tags">
                <span className="tag">{product.Category}</span>
                <span className="tag">{product.Subcategory}</span>
                <span className="tag">{product.Product_ID}</span>
              </div>

              <button className="add-to-cart-btn">Add to Cart</button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RecommendationCard;
