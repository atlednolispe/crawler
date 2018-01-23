from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
from .atlednolispe_account import smtp_server, smtp_port, sender, receiver, password
# from .account import xxx
# can't direct run the file
# use *python -m send_email.test_email* to run the script
# ref: https://stackoverflow.com/questions/72852/how-to-do-relative-imports-in-python/73149#73149


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


msg = MIMEText('Crawler Exception', 'plain', 'utf-8')
msg['From'] = _format_addr('Crawler1 <%s>' % sender)
msg['To'] = _format_addr('Administrator <%s>' % receiver)
msg['Subject'] = Header("Crawler1's State", 'utf-8').encode()

# smtp.qq.com:465 can't connect! smtp.163.com:25 istead.
server = smtplib.SMTP(smtp_server, port=smtp_port)
server.login(sender, password)
server.sendmail(sender, [receiver], msg.as_string())
server.quit()