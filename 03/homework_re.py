import re

txt = """Welcome to the Regex Training Center! 

01/02/2021, 12-25-2020, 2021.03.15, 2022/04/30, 2023.06.20, and 2021.07.04. You can
also find dates with words: March 14, 2022, and December 25, 2020. 

(123) 456-7890, +1-800-555-1234, 800.555.1234, 800-555-1234, and 123.456.7890. 
Other formats include international numbers: +44 20 7946 0958, +91 98765 43210.

john.doe@example.com, jane_doe123@domain.org, support@service.net, info@company.co.uk, 
and contact.us@my-website.com. You might also find these tricky: weird.address+spam@gmail.com,
"quotes.included@funny.domain", and this.one.with.periods@weird.co.in.

http://example.com, https://secure.website.org, http://sub.domain.co, 
www.redirect.com, and ftp://ftp.downloads.com. Don't forget paths and parameters:
https://my.site.com/path/to/resource?param1=value1&param2=value2, 
http://www.files.net/files.zip, https://example.co.in/api/v1/resource, and 
https://another-site.org/downloads?query=search#anchor. 

0x1A3F, 0xBEEF, 0xDEADBEEF, 0x123456789ABCDEF, 0xA1B2C3, and 0x0. 

#FF5733, #C70039, #900C3F, #581845, #DAF7A6, and #FFC300. RGB color codes can be tricky: 
rgb(255, 99, 71), rgba(255, 99, 71, 0.5).

123-45-6789, 987-65-4321, 111-22-3333, 555-66-7777, and 999-88-7777. Note that Social 
Security numbers might also be written like 123 45 6789 or 123456789.

Let's throw in some random sentences for good measure:
- The quick brown fox jumps over the lazy dog.
- Lorem ipsum dolor sit amet, consectetur adipiscing elit.
- Jack and Jill went up the hill to fetch a pail of water.
- She sells seashells by the seashore.

1234567890, !@#$%^&*()_+-=[]{}|;':",./<>?, 3.14159, 42, and -273.15."""

date_pattern_1 = r'\d{2}[\/.-]\d{2}[\/.-]\d{4}'
date_pattern_2 = r'\d{4}[\/.-]\d{2}[\/.-]\d{2}'
date_pattern_3 = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}'
date_pattern = rf'\b(?:{date_pattern_1}|{date_pattern_2}|{date_pattern_3})\b'

email_pattern = r'\b[\w+-.]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]{2,})+\b'

url_pattern = r'\b(?:(?:ftp|https?):\/\/|www\.)(?:[-a-zA-Z0-9]+\.)+[a-zA-Z0-9]+\b(?:[\w()\[\]@:%_\+.,~#?&\/=]*)\b'

phone_pattern_1 = r'\+[- \d+]{12,}'
phone_pattern_2 = r'\d{3}(?:[-.]\d{3,4}){2}'
phone_pattern_3 = r'\(\d{3,}\)[- \d]{8,}'
phone_pattern = rf'(?:{phone_pattern_1}|{phone_pattern_2}|{phone_pattern_3})'


def process_pattern(txt, pattern, label):
    print(label)
    if items := re.findall(pattern, txt):
        for item in items:
            print('*', item)
    else:
        print('* not found')
    print()


def main():
    process_pattern(txt, date_pattern, 'Dates:')
    process_pattern(txt, email_pattern, 'Emails:')
    process_pattern(txt, url_pattern, 'URLs:')
    process_pattern(txt, phone_pattern, 'Phones:')


if __name__ == '__main__':
    main()
