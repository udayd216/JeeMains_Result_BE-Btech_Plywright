import cv2
import typing
import oracledb
import numpy as np
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from mltu.configs import BaseModelConfigs
from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder, get_cer

from bs4 import BeautifulSoup

v_process_user = 'U1'

class ImageToWordModel(OnnxInferenceModel):
    def __init__(self, char_list: typing.Union[str, list], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_list = char_list

        # Get model input details
        self.input_name = self.model.get_inputs()[0].name  # Extract input name
        self.input_shape = self.model.get_inputs()[0].shape  # Extract input shape

    def predict(self, image: np.ndarray):
        # Ensure correct width-height order for OpenCV resizing
        image = cv2.resize(image, (self.input_shape[2], self.input_shape[1]))  
        image_pred = np.expand_dims(image, axis=0).astype(np.float32)
        preds = self.model.run(None, {self.input_name: image_pred})[0]  # Use extracted input_name
        text = ctc_decoder(preds, self.char_list)[0]
        return text

def Data_Xpath_Elements():
    v_AppNo = driver.find_element(By.XPATH, '//*[@id="tableToPrint"]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]').text
    v_RollNo = driver.find_element(By.XPATH, '//*[@id="tableToPrint"]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[1]/td[4]').text	
    v_CName = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]").text
    v_MName = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]").text
    v_FName = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]").text
    v_Category = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[5]/td[2]").text
    v_PwBD = driver.find_element(By.XPATH, '//*[@id="tableToPrint"]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[5]/td[4]').text
    v_Gender = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[6]/td[2]").text
    v_DoB = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[6]/td[4]").text
    v_StateofEligibility = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[7]/td[2]").text
    v_Nationality = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[3]/td/table/tbody/tr[7]/td[4]").text

    v_Physics = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[5]/td/table/tbody/tr[2]/td[2]").text
    v_Chemistry = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[5]/td/table/tbody/tr[3]/td[2]").text
    v_Mathematics = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[5]/td/table/tbody/tr[4]/td[2]").text
    v_Total = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[5]/td/table/tbody/tr[5]/td[2]").text
    v_TotinWords = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/table/tbody/tr[5]/td/table/tbody/tr[6]/td[2]").text

    insert_stu_dtls = \
                "INSERT INTO O_JEEMAINS_RESULTS_25 (ADMNO, APPNO, ROLLNO_SESS1, CANDIDATE_NAME, DOB, GENDER, MOTHER, FATHER, CATEGORY, PWBD, STATEOFELIGIBILITY, NATIONALITY, MATHEMATICS, PHYSICS, CHEMISTRY, TOTAL, TOTAL_IN_WORDS, PROCESS_STATUS, PROCESS_USER) \
                VALUES ('" + str(v_AdmNo) + "', '" + str(v_AppNo) + "', '" + str(v_RollNo) + "', '" + str(v_CName) + "', '" + str(v_DoB) + "', '" + str(v_Gender) + "', '" + str(v_MName) + "', '" + str(v_FName) + "', '" + str(v_Category) + "', '" + str(v_PwBD) + "', '" + str(v_StateofEligibility) + "', '" + str(v_Nationality) + "', '" + v_Mathematics + "', '" + v_Physics + "', '" + v_Chemistry + "', '" + v_Total + "', '" + str(v_TotinWords) + "', 'D', '" + str(v_process_user) + "')"      
    cur.execute(insert_stu_dtls) # Execute an INSERT statement

    update_IpStatus = "UPDATE I_JEEMAINS_RESULTS_PWD_25 SET PROCESS_STATUS = 'D', PROCESS_USER = '"+ str(v_process_user) +"', CREATEDDATE = SYSDATE WHERE APPNO = '"+ str(v_appno) +"'"
    cur.execute(update_IpStatus) # Execute an UPDATE statement
    conn.commit()
    
max_attempts = 20
attempts = 0
login_successful = False
    
#oracledb.init_oracle_client()
oracledb.init_oracle_client(lib_dir=r"D:\app\udaykumard\product\instantclient_23_6")
conn = oracledb.connect(user='RESULT', password='LOCALDEV', dsn='192.168.15.196:1521/orcldev')
cur = conn.cursor()

driver = webdriver.Chrome()
driver.maximize_window()

str_dataslot = "SELECT PROCESS_USER, START_VAL, END_VAL FROM DATASLOTS_VAL_USER WHERE PROCESS_USER = '"+v_process_user+"'"
cur.execute(str_dataslot)
res_dataslot = cur.fetchall()

start_sno = res_dataslot[0][1]
end_sno = res_dataslot[0][2]

Sno = start_sno

str_Jeeappno = "SELECT SNO, TRIM(APPNO) APPNO, TRIM(PASSWORD) PASSWORD, ADMNO FROM I_JEEMAINS_RESULTS_PWD_25 \
            WHERE PROCESS_STATUS = 'P' AND PASSWORD IS NOT NULL AND LENGTH(APPNO) = 12 AND \
            SNO >= '"+str(start_sno)+"' AND  SNO <='"+str(end_sno)+"' ORDER BY SNO"
cur.execute(str_Jeeappno)
res = cur.fetchall()

for row in res:
    v_appno = row[1]     
    v_password = row[2]
    v_AdmNo = row[3]
            
    try:  
        driver.get("https://examinationservices.nic.in/resultservices/JEEMAIN2025S1P1/Login")
        
        i_regno = driver.find_element(By.ID, "txtAppNo")      
        i_regno.send_keys(v_appno)

        i_password = driver.find_element(By.ID, "txtPassword")
        i_password.send_keys(v_password)

        Captchaimg = driver.find_element(By.ID, "capimage")
        driver.execute_script("arguments[0].scrollIntoView(true);", Captchaimg)
        Captchaimg.screenshot('Screenshotcaptcha.png')

        configs = BaseModelConfigs.load("Models/02_captcha_to_text/202502191616/configs.yaml")
        model = ImageToWordModel(model_path=configs.model_path, char_list=configs.vocab)

        image = cv2.imread('Screenshotcaptcha.png')
        prediction_text = model.predict(image)

        i_Captcha = driver.find_element(By.ID, "Captcha1")      
        i_Captcha.send_keys(prediction_text)
        
        #Button press
        Submit_button = driver.find_element(By.ID, 'Submit')
        driver.execute_script("arguments[0].click();", Submit_button)
            
        try:
            v_Captcha = driver.find_element(By.XPATH, '/html/body/form/div[2]/div[2]/div/fieldset/div/div/div[5]/div[2]/span').text                  
        except:
            v_Captcha = ''

        try:
            v_invalid = driver.find_element(By.XPATH, '/html/body/form/div[2]/div[2]/div/fieldset/div/div/div[5]/div[2]/div').text 
        except:
            v_invalid = ''
                          
        if v_Captcha == "Invalid CAPTCHA":
            while attempts < max_attempts and not login_successful:
                Captchaimg = driver.find_element(By.ID, "capimage")
                driver.execute_script("arguments[0].scrollIntoView(true);", Captchaimg)
                Captchaimg.screenshot('Screenshotcaptcha.png')

                configs = BaseModelConfigs.load("Models/02_captcha_to_text/202502191616/configs.yaml")
                model = ImageToWordModel(model_path=configs.model_path, char_list=configs.vocab)

                image = cv2.imread('Screenshotcaptcha.png')
                prediction_text = model.predict(image)
                
                i_Captcha = driver.find_element(By.ID, "Captcha1")  
                i_Captcha.clear()    
                i_Captcha.send_keys(prediction_text)
                
                #Button press
                Submit_button = driver.find_element(By.ID, 'Submit')
                driver.execute_script("arguments[0].click();", Submit_button)

                try:
                    Data_Xpath_Elements()
                    login_successful = True  
                except:
                    try:
                        v_invalid = driver.find_element(By.XPATH, '/html/body/form/div[2]/div[2]/div/fieldset/div/div/div[5]/div[2]/div').text 
                    except:
                        v_invalid = ''

                    if v_invalid == "Invalid Application Number/Password":        
                        update_IpStatus = "UPDATE I_JEEMAINS_RESULTS_PWD_25 SET PROCESS_STATUS = 'Invalid', PROCESS_USER = '"+ str(v_process_user) +"', CREATEDDATE = SYSDATE, ERROR_MESSAGE = '"+ str(v_invalid) +"' WHERE APPNO = '"+ str(v_appno) +"'"
                        cur.execute(update_IpStatus) # Execute an UPDATE statement
                        conn.commit()
                        login_successful=True
                    else:
                        login_successful=False

        elif v_invalid == "Invalid Application Number/Password":        
            update_IpStatus = "UPDATE I_JEEMAINS_RESULTS_PWD_25 SET PROCESS_STATUS = 'Invalid', PROCESS_USER = '"+ str(v_process_user) +"', CREATEDDATE = SYSDATE, ERROR_MESSAGE = '"+ str(v_invalid) +"' WHERE APPNO = '"+ str(v_appno) +"'"
            cur.execute(update_IpStatus) # Execute an UPDATE statement
            conn.commit()
            pass
        else:
            Data_Xpath_Elements()
            login_successful = True
    except:
        pass

driver.quit()
                                    


