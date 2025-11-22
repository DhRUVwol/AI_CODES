# gaussian_hmm_finance.py
import numpy as np, pandas as pd
from hmmlearn.hmm import GaussianHMM
import matplotlib.pyplot as plt

def log_returns(prices):
    return np.log(prices).diff().dropna()

def fit_hmm(returns, n_states=2):
    model = GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=2000, random_state=42)
    model.fit(returns.values.reshape(-1,1))
    hidden_states = model.predict(returns.values.reshape(-1,1))
    return model, hidden_states

if __name__ == "__main__":
    # Example: generate synthetic price data if yahoo not available
    np.random.seed(0)
    # Simulated regime shifts: state 0 low vol, state1 high vol
    T=1000
    states = np.random.choice([0,1], size=T, p=[0.9,0.1])
    returns = np.where(states==0, np.random.normal(0,0.01,T), np.random.normal(0,0.05,T))
    dates = pd.date_range("2010-01-01", periods=T)
    returns = pd.Series(returns, index=dates)
    model, hidden = fit_hmm(returns, n_states=2)
    print("Means:", model.means_.ravel())
    print("Vars:", np.array([np.diag(cov) for cov in model.covars_]).ravel())
    # plot
    plt.figure(figsize=(12,4))
    plt.plot(returns.index, returns.values, label='log-returns')
    plt.scatter(returns.index, returns.values, c=hidden, cmap='viridis', s=6)
    plt.title("Returns colored by HMM state")
    plt.show()
