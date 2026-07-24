import { useState } from 'react'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setError('')
    setResult(null)

    if (!url.trim()) {
      setError('Entre une URL')
      return
    }

    setLoading(true)
    try {
      const res = await fetch('/api/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      })

      if (!res.ok) throw new Error('Erreur serveur')

      const data = await res.json()
      setResult(data)
      setUrl('')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const shortLink = result
    ? `${window.location.origin}/${result.code}`
    : ''

  return (
    <div className="container">
      <h1>URL Shortener</h1>
      <p className="subtitle">Colle une URL longue, récupère un lien court.</p>

      <div className="form">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
          placeholder="https://exemple.com/une/url/tres/longue"
        />
        <button onClick={handleSubmit} disabled={loading}>
          {loading ? '...' : 'Raccourcir'}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <span className="label">Ton lien court</span>
          <a href={shortLink} target="_blank" rel="noreferrer">
            {shortLink}
          </a>
          <a className="stats-link" href={`/api/stats/${result.code}`} target="_blank" rel="noreferrer">
            Voir les statistiques
          </a>
        </div>
      )}
    </div>
  )
}

export default App