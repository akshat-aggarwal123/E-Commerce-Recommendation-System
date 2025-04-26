import { useState } from 'react';
import { getRecommendations } from '../services/api';

const SearchBar = ({ onRecommendationsLoaded }) => {
  const [customerId, setCustomerId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const recommendations = await getRecommendations(customerId, 5);
      onRecommendationsLoaded(recommendations);
    } catch (err) {
      setError('Failed to fetch recommendations. Check the customer ID and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <input
        type="text"
        placeholder="Enter Customer ID (e.g., C3805)"
        value={customerId}
        onChange={(e) => setCustomerId(e.target.value)}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Loading...' : 'Get Recommendations'}
      </button>
      {error && <p className="error-message">{error}</p>}
    </form>
  );
};

export default SearchBar;