
def getTitle(context, page):
    return context.browser.find_elements_by_css_selector(
        "h2.entry-title a:first-child" if page == "dzirkstele" else "h2 a[itemprop='url']")


def getDescription(context, page):
    return context.browser.find_elements_by_css_selector(
        ".entry-summary" if page == "dzirkstele" else "div[itemprop='blogPost'] p")
            
def getDate(context, page):
    return context.browser.find_elements_by_css_selector(
        ".entry-date")


def cookieAgreement(context):
 return context.browser.find_element_by_css_selector(
    "button[aria-label='PIEKRĪTU']")