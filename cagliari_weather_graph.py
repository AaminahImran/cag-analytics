"""
Cagliari Weather Graph - January 2025
This script creates a line graph showing simulated daily temperature data for Cagliari in January 2025.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import webbrowser
from datetime import datetime, timedelta

def generate_cagliari_january_data():
    """
    Generate simulated weather data for Cagliari in January 2025.
    Cagliari typically has mild winters with temperatures around 8-15°C in January.
    
    Returns:
        tuple: (dates, temperatures, precipitation)
    """
    # Start date: January 1, 2025
    start_date = datetime(2025, 1, 1)
    
    # Generate dates for all of January
    dates = [start_date + timedelta(days=i) for i in range(31)]
    date_labels = [d.strftime("%d-%b") for d in dates]
    
    # Generate realistic but simulated temperatures for Cagliari in January
    # Base temperature around 12°C with some random variation
    base_temp = 12
    np.random.seed(2025)  # For reproducibility
    
    # Create a slight trend (cooler at beginning and end of month, warmer in middle)
    trend = -np.abs(np.linspace(-2, 2, 31)) + 2
    
    # Add random daily variation
    daily_variation = np.random.normal(0, 2, 31)
    
    # Combine for final temperatures
    temperatures = base_temp + trend + daily_variation
    
    # Generate precipitation data (mm of rain)
    # Cagliari gets around 50mm of rain in January, spread across ~7 rainy days
    precipitation = np.zeros(31)
    rainy_days = np.random.choice(range(31), 7, replace=False)
    precipitation[rainy_days] = np.random.gamma(shape=2, scale=7, size=7)
    
    return date_labels, temperatures, precipitation

def create_cagliari_weather_graph():
    """
    Create and save a graph of Cagliari's simulated January 2025 weather.
    
    Returns:
        str: Path to the saved HTML file
    """
    dates, temperatures, precipitation = generate_cagliari_january_data()
    
    # Create figure with two subplots (temperature and precipitation)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    # Temperature plot
    ax1.plot(dates, temperatures, 'o-', color='#FF5733', linewidth=2, markersize=6)
    ax1.set_title('Simulated Daily Temperatures in Cagliari - January 2025', fontsize=16)
    ax1.set_ylabel('Temperature (°C)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add temperature annotations for a few points
    for i in [0, 10, 20, 30]:
        if i < len(temperatures):
            ax1.annotate(f'{temperatures[i]:.1f}°C', 
                        xy=(i, temperatures[i]), 
                        xytext=(0, 10),
                        textcoords='offset points',
                        ha='center')
    
    # Precipitation plot
    bars = ax2.bar(dates, precipitation, color='#3498DB', alpha=0.7)
    ax2.set_ylabel('Precipitation (mm)', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
    ax2.tick_params(axis='x', rotation=45)
    
    # Add some annotations for rainy days
    for i, p in enumerate(precipitation):
        if p > 0:
            ax2.annotate(f'{p:.1f}mm', 
                        xy=(i, p), 
                        xytext=(0, 5),
                        textcoords='offset points',
                        ha='center',
                        fontsize=8)
    
    plt.tight_layout()
    
    # Save the graph
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"cagliari_weather_january_2025_{timestamp}.html"
    img_filename = f"cagliari_weather_january_2025_{timestamp}.png"
    
    # Save as PNG for embedding
    plt.savefig(img_filename)
    
    # Create HTML file with the image and additional information
    with open(filename, 'w') as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cagliari Weather - January 2025</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                .container {{ max-width: 1000px; margin: 0 auto; }}
                h1 {{ color: #2C3E50; text-align: center; }}
                img {{ max-width: 100%; height: auto; display: block; margin: 20px auto; border: 1px solid #ddd; }}
                .info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }}
                .note {{ font-style: italic; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Cagliari Weather Forecast - January 2025</h1>
                
                <img src="{img_filename}" alt="Cagliari Weather Graph">
                
                <div class="info">
                    <h2>Weather Summary</h2>
                    <p>This graph shows simulated daily temperatures and precipitation for Cagliari, Sardinia in January 2025.</p>
                    
                    <h3>Key Observations:</h3>
                    <ul>
                        <li>Average temperature: {np.mean(temperatures):.1f}°C</li>
                        <li>Highest temperature: {np.max(temperatures):.1f}°C</li>
                        <li>Lowest temperature: {np.min(temperatures):.1f}°C</li>
                        <li>Total precipitation: {np.sum(precipitation):.1f}mm</li>
                        <li>Number of rainy days: {np.sum(precipitation > 0)}</li>
                    </ul>
                    
                    <p class="note">Note: This is simulated data based on historical weather patterns for Cagliari in January.
                    Actual weather conditions in January 2025 may differ.</p>
                </div>
            </div>
        </body>
        </html>
        """)
    
    return filename

def main():
    """Generate the weather graph and open it in a browser."""
    print("Generating Cagliari weather graph for January 2025...")
    html_file = create_cagliari_weather_graph()
    print(f"Graph created: {html_file}")
    
    # Open the graph in the default web browser
    try:
        webbrowser.open('file://' + os.path.abspath(html_file))
        print("Graph opened in your web browser.")
    except Exception as e:
        print(f"Error opening graph: {str(e)}")
        print(f"Please open the file manually: {os.path.abspath(html_file)}")

if __name__ == "__main__":
    main()
