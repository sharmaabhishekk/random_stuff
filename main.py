from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException

def get_match_data(base_url):
    
    """Scrapes the pitch canvas element of a match page to return the x,y data

    Arguments:
        base_url
    Returns:
        data_dict = dict of scraped data
    """
    driver.get(base_url)
    time.sleep(15)

    ##Find and click the "Events & Stats" tab
    _ = driver.find_element_by_xpath("/html/body/div[1]/section/myapp/section/div/div/div/div/section/div/div/div[2]/div[1]/div/ul/li[4]") 
    _.click()
    time.sleep(5)

    data_dict = {"A":{}, "B":{}}
    data_dict["A"]["team_name"] = base_url.split("matchcentre/")[-1].split("vs")[0].split("-", 1)[-1][:-1]
    data_dict["B"]["team_name"] = base_url.split("matchcentre/")[-1].split("vs")[-1][1:]

    all_info_elms = driver.find_elements_by_css_selector("div[class='si-mc-evntSats-fItem']")
    for element in all_info_elms:
        try:
            pitch_element = element.find_element_by_css_selector("div[class='si-mc-evntSats-ptch']")
            var_name = element.find_element_by_css_selector("div[class='si-mc-evntSats-title']").text ##type of event: Shot OT/Shot off T/Goal/Offside etc
            
            for team_char in ['A', 'B']:
                xs = []; ys = []
                e = pitch_element.find_elements_by_css_selector(f"div[class='si-mc-evntSats-plot si-mc-plot-team{team_char}']")
                for event_elm in e:
                    x,y = event_elm.get_attribute("data-left"), event_elm.get_attribute("data-top")
                    xs.append(x); ys.append(y)
                data_dict[team_char][var_name] = [xs, ys]    
            
        except NoSuchElementException:
            pass
        
    return data_dict


def get_match_links():
    """Collects all match_centre urls of the matches played so far

    Returns:
        links - list of all match_urls found
    """
    driver.get("https://www.indiansuperleague.com/schedule-fixtures")
    time.sleep(7)

    match_centre_elements = driver.find_elements_by_css_selector("a[class='si-btn si-btn-secondary-outline si-btn-radius']")
    
    links = []
    for element in match_centre_elements:
        try:
            links.append(element.get_property("href"))
        except:
            pass
        
    return links

if __name__== "__main__":
    driver = webdriver.Chrome() ##instantiate driver

    data = []
    match_urls = get_match_links()
    for match_url in match_urls:
        data.append(get_match_data(match_url))
