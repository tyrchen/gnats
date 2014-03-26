import base64
from gnats.items import GnatsItem
from dateutil.parser import parse
from pw import user, password

def get_text(hxs, xpath):
    try:
        return hxs.select('%s/text()' % xpath).extract()[0].strip()
    except:
        return ''

def get_last_updater(hxs):
    s = get_text(hxs, '//*[@id="audit-trail"]//div[contains(@class, "section-hdg")][last()]')
    try:
        return s.split('@')[0].strip()
    except:
        return ''

def parse_gnats_item(hxs, scope=1):
    item = GnatsItem()
    item['number'] = get_text(hxs, '//*[@id="val_number"]')
    if scope > 1:
        item['number'] += '-%s' % scope
    item['title'] = get_text(hxs, '//*[@id="val_synopsis"]')
    item['responsible'] = get_text(hxs, '//*[@id="val_responsible_%s"]/a' % scope)
    item['state'] = get_text(hxs, '//*[@id="val_state_%s"]' % scope)
    item['reported_in'] = get_text(hxs, '//*[@id="val_reported-in"]')
    item['submitter'] = get_text(hxs, '//*[@id="val_submitter-id"]')
    item['category'] = get_text(hxs, '//*[@id="val_category"]/a')
    item['level'] = get_text(hxs, '//*[@id="val_problem-level"]')
    item['platform'] = get_text(hxs, '//*[@id="val_platform"]')
    item['originator'] = get_text(hxs, '//*[@id="val_originator"]')
    item['customer'] = get_text(hxs, '//*[@id="val_customer"]')
    item['qa_owner'] = get_text(hxs, '//*[@id="val_systest-owner_%s"]/a' % scope)
    item['ce_owner'] = get_text(hxs, '//*[@id="val_customer-escalation-owner"]/a')
    item['dev_owner'] = get_text(hxs, '//*[@id="val_dev-owner_%s"]/a' % scope)
    item['audit_trail'] = hxs.select('//*[@id="audit-trail"]').extract()[0].strip()
    item['last_audit'] = get_text(hxs, '//*[@id="audit-trail"]//div[@class="section-contents"][last()]/pre')
    item['last_updater'] = get_last_updater(hxs)
    item['arrived_at'] = parse(get_text(hxs, '//*[@id="val_arrival-date"]'))
    item['modified_at'] = parse(get_text(hxs, '//*[@id="val_last-modified"]'))
    item['crawled'] = True
    item['worker'] = []
    return item

def get_password():
    return user, base64.b64decode(password)