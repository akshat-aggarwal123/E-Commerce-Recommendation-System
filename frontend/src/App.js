import { useState } from 'react';
import SearchBar from './components/SearchBar';
import RecommendationList from './components/RecommendationList';
import './styles.css';

function App() {
  const [recommendations, setRecommendations] = useState([]);

  return (
    <div className="app-container">
      <h1>Personalized Product Recommendations</h1>
      <SearchBar onRecommendationsLoaded={setRecommendations} />
      {recommendations.length > 0 && (
        <>
          <h2>Top Recommendations</h2>
          <RecommendationList recommendations={recommendations} />
        </>
      )}
    </div>
  );
}

export default App;