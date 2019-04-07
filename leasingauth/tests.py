from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
class SuperAdminTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']
    @classmethod
    def setUpClass(self):
        super(StaticLiveServerTestCase, self).setUpClass()
        self.selenium = webdriver.PhantomJS('/home/naresh/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        self.selenium.maximize_window()
        self.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SuperAdminTests, cls).setUpClass()

    def test_super_user_login(self):
        #go to super admin login page
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #enter user name
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('zack')
        #enter password
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('jack@123')
        #click login
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(2)
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="content"]/h1').text, 'Site administration')

    def test_add_leasing_client(self):
        #Login SuperUser
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #enter user name
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('zack')
        #enter password
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('jack@123')
        #click login
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(2)
        #click on leasing client
        self.selenium.find_element_by_xpath('//*[@id="content-main"]/div[4]/table/tbody/tr[1]/th/a').click()
        #click on add leasingclient
        self.selenium.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()
        #enter values
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('naresh')
        self.selenium.find_element_by_xpath('//*[@id="id_email"]').send_keys('naresh@gmail.com')
        self.selenium.find_element_by_xpath('//*[@id="id_password1"]').send_keys('naresh@123')
        self.selenium.find_element_by_xpath('//*[@id="id_password2"]').send_keys('naresh@123')
        #click save btn
        self.selenium.find_element_by_xpath('//*[@id="leasingclient_form"]/div/div/input[1]').click()
        #enter values
        self.selenium.find_element_by_xpath('//*[@id="id_first_name"]').send_keys('naresh')
        #click save btn
        self.selenium.find_element_by_xpath('//*[@id="leasingclient_form"]/div/div/input[1]').click()

        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="container"]/ul/li').text, 'The leasing client "naresh@gmail.com" was changed successfully.')

    def test_add_leasing_client_validation(self):
        #Login SuperUser
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #enter user name
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('zack')
        #enter password
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('jack@123')
        #click login
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(2)
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="content"]/h1').text, 'Site administration')

        #go to add leasing client
        self.selenium.get('%s%s' % (self.live_server_url, '/leasingauth/leasingclient/add/'))
        #click save
        self.selenium.find_element_by_xpath('//*[@id="leasingclient_form"]/div/div/input[1]').click()
        
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="leasingclient_form"]/div/p').text,'Please correct the errors below.')

    def test_add_leasing_client_invite_token(self):
        #Login SuperUser
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #enter user name
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('zack')
        #enter password
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('jack@123')
        #click login
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(2)
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="content"]/h1').text, 'Site administration')
        
        #go to add invite token
        self.selenium.get('%s%s' % (self.live_server_url, '/leasingauth/leasingclientinvitetoken/add/'))
        #enter invite tokenAA
        self.selenium.find_element_by_xpath('//*[@id="id_invite_token"]').send_keys('test_token')
        #click save
        self.selenium.find_element_by_xpath('//*[@id="leasingclientinvitetoken_form"]/div/div/input[1]').click()

        time.sleep(2)

        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/td[2]').text,'test_token')

    def test_add_leasing_client_invite_token_validation(self):
        #Login SuperUser
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #enter user name
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('zack')
        #enter password
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('jack@123')
        #click login
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(2)
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="content"]/h1').text, 'Site administration')
        
        #go to add invite token
        self.selenium.get('%s%s' % (self.live_server_url, '/leasingauth/leasingclientinvitetoken/add/'))
        #click save
        self.selenium.find_element_by_xpath('//*[@id="leasingclientinvitetoken_form"]/div/div/input[1]').click()

        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="leasingclientinvitetoken_form"]/div/p').text,'Please correct the error below.')

    def test_add_export_result(self):
        #Login SuperUser
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #enter user name
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('zack')
        #enter password
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('jack@123')
        #click login
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(2)
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="content"]/h1').text, 'Site administration')

        #click on export result
        self.selenium.find_element_by_xpath('//*[@id="content-main"]/div[3]/table/tbody/tr[4]/th/a').click()
        #click on add export
        self.selenium.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()
        #enter values
        self.selenium.find_element_by_xpath('//*[@id="id_clause_number"]').send_keys('1')
        self.selenium.find_element_by_xpath('//*[@id="id_clause_name"]').send_keys('clause name 1')
        #click save btn
        self.selenium.find_element_by_xpath('//*[@id="exportresult_form"]/div/div/input[1]').click()
        
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="container"]/ul/li').text, 'The export result "1" was added successfully.')

    def test_add_Descriptions(self):
        #Login SuperUser
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #enter user name
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('zack')
        #enter password
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('jack@123')
        #click login
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(2)
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="content"]/h1').text, 'Site administration')

        #go to add description
        self.selenium.get('%s%s' % (self.live_server_url, '/leasingapi/description/add/'))
        #enter values
        self.selenium.find_element_by_xpath('//*[@id="id_text"]').send_keys('desc1')
        #click save btn
        self.selenium.find_element_by_xpath('//*[@id="description_form"]/div/div/input[1]').click()

        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="container"]/ul/li').text, 'The description "1 - desc1" was added successfully.')

    def test_add_key_text(self):
        #Login SuperUser
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #enter user name
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('zack')
        #enter password
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('jack@123')
        #click login
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(2)
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="content"]/h1').text, 'Site administration')

        #go to add key text
        self.selenium.get('%s%s' % (self.live_server_url, '/leasingapi/keytext/add/'))
        #enter values
        self.selenium.find_element_by_xpath('//*[@id="id_content"]').send_keys('key1')
        #click save btn
        self.selenium.find_element_by_xpath('//*[@id="keytext_form"]/div/div/input[1]').click()

        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="container"]/ul/li').text, 'The key text "key1" was added successfully.')

    def test_add_legal_position(self):
        #Login SuperUser
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #enter user name
        self.selenium.find_element_by_xpath('//*[@id="id_username"]').send_keys('zack')
        #enter password
        self.selenium.find_element_by_xpath('//*[@id="id_password"]').send_keys('jack@123')
        #click login
        self.selenium.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(2)
        self.assertEqual(self.selenium.find_element_by_xpath('//*[@id="content"]/h1').text, 'Site administration')

        #go to add description
        self.selenium.get('%s%s' % (self.live_server_url, '/leasingapi/description/add/'))
        #enter values
        self.selenium.find_element_by_xpath('//*[@id="id_text"]').send_keys('desc1')
        #click save btn
        self.selenium.find_element_by_xpath('//*[@id="description_form"]/div/div/input[1]').click()

        #go to add key text
        self.selenium.get('%s%s' % (self.live_server_url, '/leasingapi/keytext/add/'))
        #enter values
        self.selenium.find_element_by_xpath('//*[@id="id_content"]').send_keys('key1')
        #click save btn
        self.selenium.find_element_by_xpath('//*[@id="keytext_form"]/div/div/input[1]').click()

        #go to add legal_postions
        self.selenium.get('%s%s' % (self.live_server_url, '/leasingapi/legalposition/add/'))
        time.sleep(2)
        #select client
        self.selenium.find_element_by_xpath('//*[@id="id_client"]').click()
        self.selenium.find_element_by_xpath('//*[@id="id_client"]/option[2]').click()
        #select clause name
        self.selenium.find_element_by_xpath('//*[@id="id_clause_name"]/option').click()
        #select clause text
        self.selenium.find_element_by_xpath('//*[@id="id_text"]/option').click()
        #enter region
        self.selenium.find_element_by_xpath('//*[@id="id_reason"]').send_keys('region1')
        #click save btn
        self.selenium.find_element_by_xpath('//*[@id="id_reason"]').click()
