
def getTitle(context, page):
    return context.browser.find_elements_by_css_selector(
        ".news.articles .namelink" if page == "dzirkstele" else "h2 a[itemprop='url']")


def getDescription(context, page):
    return context.browser.find_elements_by_css_selector(
        ".news.articles .intro" if page == "dzirkstele" else "div[itemprop='blogPost'] p")


def cookieAgreement(context):
 return context.browser.find_element_by_css_selector(
    "button[aria-label='PIEKRĪTU']")
