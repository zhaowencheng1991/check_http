#!/usr/bin/python
# coding: utf-8
# author  :zhaowencheng
# desc    :checck suda http service

import httplib
import socket
import subprocess
from conf import host_conf

host = host_conf.host_l
socket.setdefaulttimeout(30)

def check_http(host,method,url):
    conn = httplib.HTTPConnection(host)
    conn.request(method,url)
    result = conn.getresponse()
    status = result.status
    if status == 200:
        return False
    return True

def allert_sms(message):
    message = str(message)
    level = 'warning'
    service = 'SUDA_NGINX'
    subject = 'suda前端机nginx服务异常'
    sms = 'http://monitor.pso.sina.com.cn/monitor/index.php/interface/sendSMS'
    receiver = 'wencheng'

    curl_cmd = ("curl -d receivers=%s -d service=%s -d level=%s -d subject='%s' %s") % (
    receiver, service, level, message, sms)
    try_run_ing = subprocess.Popen(curl_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def allert_mail(message):
    message = str(message)
    level = 'warning'
    service = 'SUDA_NGINX'
    subject = 'suda前端机nginx服务异常'
    mail = 'http://monitor.pso.sina.com.cn/monitor/index.php/interface/sendMail'
    receiver = 'wencheng'
    curl_cmd = ("curl -d receivers=%s -d service=%s -d level=%s -d subject=%s -d content='%s', %s") % (
    receiver, service, level, subject, message, mail)
    try_run_ing = subprocess.Popen(curl_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    alert_list = []
    for host_ip in host:
        check_result = check_http(host_ip, "GET", "/ga.gif")
        if check_result:
            alert_list.append(host_ip)

    if alert_list:
        message = (" %s : %s " % ("suda nginx 异常ip", alert_list))
        allert_sms(message)
        allert_mail(message)
        print  (" %s : %s " % ("check ngin error", alert_list))
    else:
        print "che_suda_ok "