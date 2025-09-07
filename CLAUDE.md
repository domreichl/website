# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a personal portfolio website with a Single Page Application (SPA) architecture using vanilla JavaScript. The site showcases work across three main domains: Machine Learning, Cognitive Science, and Philosophy.

### Core Architecture Components

- **Frontend**: Static HTML/CSS/JS with AJAX-based navigation via `script.js:20-47`
- **Backend Services**: Python Flask applications for interactive features
- **Content Structure**: Modular page system with expandable content blocks

### Key Files and Structure

- `index.html` - Main entry point with navigation header and content container
- `script.js` - Core SPA functionality including navigation, AJAX loading, and history management
- `styles.css` - Complete styling including responsive design and dark theme
- `home.html` - Landing page with three expandable content sections
- `about.html` - Contact and profile information
- `pages/` - Content pages organized by domain (ml/, cogsci/, philo/)
- `apps/` - Backend Python applications for interactive features

### Navigation System

The site uses a custom SPA system in `script.js` that:
- Loads content via AJAX without full page refreshes (`script.js:7-17`)
- Manages browser history and back/forward navigation (`script.js:40-47`) 
- Handles initial page routing based on URL (`script.js:26-38`)

### Interactive Applications

**Stock Price Prediction App** (`apps/forecast/`)
- Machine learning models for stock price forecasting
- Uses TensorFlow, XGBoost, LightGBM, and Prophet
- Main entry point: `apps/forecast/main.py`
- Models stored in `apps/forecast/models/`

**Philosophical Text Generator** (`apps/llm/`)
- Flask API using Hugging Face Llama model
- Generates philosophical text in Spinoza's style
- Endpoint: `/run-python` for POST requests

**Graph Visualization** (`apps/graph/`)
- Displays stock prediction results
- Embedded iframe in stock price prediction page

## Development Commands

Since this is a static website with Python backend services, there are no standard build commands. Development involves:

**For the main website:**
- Serve static files via any HTTP server
- No build process required for frontend

**For Python applications:**
- Install dependencies: `pip install -r apps/[app_name]/requirements.txt`
- Run Flask apps directly: `python apps/[app_name]/app.py`
- Stock prediction: `python apps/forecast/main.py`

## Content Management

Content is organized into three main categories accessible via expandable blocks on the home page:
- **Machine Learning**: Text generation, stock prediction, computer vision
- **Cognitive Science**: Bayesian brain theory, placebo effects, emotions research  
- **Philosophy**: Glossaries, concepts, principles

Pages use consistent styling classes:
- `.blog-content` - Standard article layout with white background
- `.app-content` - Centered layout for interactive applications
- `.page-content` - Multi-column layout for information pages

## Responsive Design

The site includes mobile-responsive breakpoints at 768px with:
- Adjusted padding and layout for mobile devices
- Modified header spacing and navigation
- Responsive image and content scaling