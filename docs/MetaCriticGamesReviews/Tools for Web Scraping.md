Before selecting tools, it's essential to understand the project's specific needs, such as the complexity of the websites to be scraped (dynamic content, JavaScript-heavy sites, etc.), rate limiting concerns, and the need for data parsing and storage capabilities.

# Target Website
Our target website will be the [games section of Metacritic.com](https://www.metacritic.com/game/). It's a mix of static and dynamic content.

## Website Complexity
The content that's interesting for us can be found in three types of section:
- Games list: this content is mostly static, and extracting it won't be a problem.
- Game Info: we'll extract the information data for each games previously collected from their specific page, as most of the content is also static.
- Game users reviews: things become complex here, as these pages load review data dynamically from an API endpoint.

## Rate Limits and Bot Access
We'll be nice and respect the robots.txt of the site. It's pretty simple though. Here's the full file content:

```
User-agent: *
Disallow: /search
Disallow: /signup
Disallow: /login
Disallow: /user
Disallow: /jl/
# Google is crawling the Ad defineSlot() parameters.  Exclude them so we don't get a bunch of 404s.
Disallow: /8264/
Disallow: /7336/

Sitemap: https://www.metacritic.com/news/latest.xml
Sitemap: https://www.metacritic.com/news/index.xml
Sitemap: https://www.metacritic.com/galleries/index.xml
Sitemap: https://www.metacritic.com/games.xml
Sitemap: https://www.metacritic.com/movies.xml
Sitemap: https://www.metacritic.com/tvshows.xml
Sitemap: https://www.metacritic.com/celebrities.xml
```
As we can see, pretty much the entire site is accessible by any bot user-agent, except for a few ones that, fortunately, are not interesting for us.

There aren't rate limits definitions, but we still must be careful and apply basic rate limiting and user-agent rotation strategies.

## Data Parsing
The games list and information data is scattered throughout the site in specific HTML tags, requiring HTML parsers to extract them efficiently.
The games reviews are supplied to the site by an API endpoint. So our initial strategy will be to mimic the site's call to this endpoint. The complexity of this task is unknown yet, but we must at least take measurements to avoid being banned.

## Data Storage
Initially, must of the data pipeline will run locally, but we want to leave room to improvements, like sending the data to a cloud storage service.
Also, we won't do an extensive extraction. So storage size won't be a problem.

# Tools and Frameworks
This table highlights the primary use, ease of use, support for dynamic content, community support, and features related to ethical scraping for each tool. While tools like Scrapy offer built-in support for ethical scraping practices, most others require manual compliance with such practices.

| Tool            | Primary Use                    | Ease of Use | Support for Dynamic Content | Community and Support | Ethical Scraping Features |
|-----------------|--------------------------------|-------------|-----------------------------|-----------------------|---------------------------|
| Requests        | HTTP requests                  | High        | No                          | Excellent             | Manual compliance         |
| Beautiful Soup  | HTML/XML parsing               | High        | No                          | Excellent             | Manual compliance         |
| Scrapy          | Full web scraping framework    | Medium      | Yes                         | Excellent             | Built-in support          |
| Selenium        | Web browser automation         | Medium      | Yes                         | Excellent             | Manual compliance         |
| LXML            | HTML/XML parsing               | High        | No                          | Good                  | Manual compliance         |
| Pandas          | Data analysis (HTML tables)    | High        | No                          | Excellent             | Manual compliance         |
| PyQuery         | HTML/XML parsing               | High        | No                          | Good                  | Manual compliance         |
# Veredit
We'll go for ease of use and flexibility using a combination of the requests and beatifulsoap libraries.
Scrapy could be an option, but it's too complex, and as a framework by nature, it' meant to be run as a standalone application.
Scrapy works best as an automation tool for interact with websites, and we don't need this for this project.