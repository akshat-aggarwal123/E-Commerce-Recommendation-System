// src/App.jsx
import { useState } from 'react';
import SearchBar from './components/SearchBar';
import RecommendationCard from './components/RecommendationCard';
import './index.css';

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [aiInsights, setAiInsights] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleRecommendationsLoaded = (data) => {
    setRecommendations(data);
    setIsLoading(false);
  };

  const handleInsightsLoaded = (insights) => {
    setAiInsights(insights);
  };

  const handleLoadingStateChange = (loading) => {
    setIsLoading(loading);
  };

  return (
    <div className="app-container">
      <h1>Personalized Product Recommendations</h1>
      <SearchBar
        onRecommendationsLoaded={handleRecommendationsLoaded}
        onInsightsLoaded={handleInsightsLoaded}
        onLoadingStateChange={handleLoadingStateChange}
      />

      <RecommendationCard
        recommendations={recommendations}
        aiInsights={aiInsights}
        isLoading={isLoading}
      />
    </div>
  );
}

export default App;
