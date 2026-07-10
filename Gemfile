source "https://rubygems.org"

gem "jekyll", "~> 4.3"

# Theme base. My layouts and stylesheet override almost everything it ships.
gem "jekyll-theme-chirpy", "~> 7.3"

group :jekyll_plugins do
  gem "jekyll-paginate-v2", "~> 3.0"
  gem "jekyll-archives", "~> 2.3"
  gem "jekyll-seo-tag", "~> 2.8"
  gem "jekyll-sitemap", "~> 1.4"
end

platforms :windows, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# File watcher for `jekyll serve` on Windows.
gem "wdm", "~> 0.2", platforms: [:windows]
