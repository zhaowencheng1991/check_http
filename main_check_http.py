#!/usr/bin/python
# coding: utf-8
# author  :zhaowencheng
# desc    :checck suda http service

import httplib
import socket
import subprocess
from conf import host_conf

host = host_conf.host_l
socket.setdefaulttimeout(3)
emial_list = host_conf.user_l
def check_http(host,method,url):
    try:
        conn = httplib.HTTPConnection(host)
        conn.request(method,url)
        result = conn.getresponse()
        status = result.status
        if status == 200:
            return False
        return True
    except:
        return True

def get_duty_user(host,method,url):
    try:
        conn = httplib.HTTPConnection(host)
        conn.request(method,url)
        result = conn.getresponse()
        duty_user = result.read()
    except:
        duty_user = "wencheng"
    return duty_user


def allert_sms(message):
    message = str(message)
    level = 'warning'
    service = 'SUDA_NGINX'
    subject = 'suda前端机nginx服务异常'
    sms = 'http://monitor.pso.sina.com.cn/monitor/index.php/interface/sendSMS'
    receiver = emial_list

    curl_cmd = ("curl -d receivers=%s -d service=%s -d level=%s -d subject='%s' %s") % (
    receiver, service, level, message, sms)
    try_run_ing = subprocess.Popen(curl_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def allert_mail(message):
    message = str(message)
    level = 'warning'
    service = 'SUDA_NGINX'
    subject = 'suda前端机nginx服务异常'
    mail = 'http://monitor.pso.sina.com.cn/monitor/index.php/interface/sendMail'
    receiver = emial_list
    curl_cmd = ("curl -d receivers=%s -d service=%s -d level=%s -d subject=%s -d content='%s', %s") % (
    receiver, service, level, subject, message, mail)
    try_run_ing = subprocess.Popen(curl_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    duty_user = get_duty_user("monitor.pso.sina.com.cn", "GET", "/monitor/index.php/interface/internal/getDutyUser")
    emial_list = emial_list+duty_user
    print duty_user
    alert_list = []
    for host_ip in host:
        check_result = check_http(host_ip, "GET", "/a.gif")
        if check_result:
            alert_list.append(host_ip)

    if alert_list:
        message = (" %s : %s " % ("suda nginx 异常ip", alert_list))
        allert_sms(message)
        allert_mail(message)
        print  (" %s : %s " % ("check ngin error", alert_list))
    else:
        print "check_suda_ok "