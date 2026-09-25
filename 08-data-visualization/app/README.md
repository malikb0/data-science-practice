# Visualisation dashboard

A [Plotly Dash](https://dash.plotly.com/) app over the Gapminder panel.

## Run

```bash
make install
python scripts/download_data.py --module 08
python 08-data-visualization/app/dashboard.py      # http://127.0.0.1:8050
```

## What it shows

- A bubble chart of GDP per capita versus life expectancy, sized by population.
- A continent filter (radio buttons).
- A year slider.

`filter_data()` and the figure builder are plain functions, so they can be tested without
starting a server.

## Limitations

The Gapminder series is five-yearly and ends in 2007; the app is single-user and does not
cache.
