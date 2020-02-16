import pymysql
import xlrd
import os,random
import time


class Dissection:
    def __init__(self,filename,host,port,user,passwd,db,charset):
        self.filename=filename
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.db=db
        self.charset=charset
        data = xlrd.open_workbook(filename)
        self.data=data
        #self.connect(self.host, self.port, self.user, self.passwd, self.db, self.charset)
        #self.download(self.filename)


    def connect(self,host,port,user,passwd,db,charset):
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        cursor = conn.cursor()
        if cursor:
            print("Connection successful.")
            return conn
        else:
            print("Connection error.")

    def download(self,filename):

        data=xlrd.open_workbook(filename)
        table=data.sheets()[0]
        nrows=table.nrows
        ncols=table.ncols
        conn=self.connect(self.host, self.port, self.user, self.passwd, self.db, self.charset)
        cursor=conn.cursor()
        for i in range(1, nrows):
            sql="INSERT INTO xjtk(question,option_a,option_b,option_c,option_d,option_e,"
            sql+="question_answer,question_difclt,question_memo)"
            sql+="VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            a=table.row_values(i)
            params=(a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9])
            row=cursor.execute(sql%params)
            print(row)
            conn.commit()
        cursor.close()
        conn.close()
    def test(self):
        conn=self.connect(self.host, self.port, self.user, self.passwd, self.db, self.charset)
        cursor=conn.cursor()
        print("Enter 'enter' will start test:")
        answer=input()
        while(answer=="enter" or answer!="quit"):
            num = random.randint(1, self.nrows-1)
            sql_1 = "SELECT * FROM xjtk WHERE id='%d'"
            cursor.execute(sql_1 % num)
            result=list(cursor.fetchall())
            text = "Question:"+result[0][1]+"\n"
            text += "A:"+result[0][2]+"\n"
            text += "B:"+result[0][3]+"\n"
            text += "C:"+result[0][4]+"\n"
            text += "D:"+result[0][5]+"\n"
            text += "E:"+result[0][6]+"\n"
            print(text)
            answer=input("Please enter an answer:")
            if answer==result[0][7]:
                print("Congratulations,you got it!")
                print("-------------------------------------------------")
                print("Enter 'quit' to finish the test.")
                continue
            else:
                print("Your answer is wrong,the correct answer is:"+result[0][7])

                print("-------------------------------------------------")
                print("Enter 'quit' to finish the test.")


    def excel_test(self):
        filename=self.filename
        data=xlrd.open_workbook(filename)
        table=data.sheets()[0]
        nrows=table.nrows#行数
        ncols=table.ncols#列数



        answer = input("Enter 'enter' will start test:")
        while (answer == "enter" or answer != "quit"):
            num = random.randint(1, nrows-1)
            for i in range(1,nrows-1):
                if int(table.col_values(0)[i]) == num:
                    text="Question:"+table.row_values(i+1)[1]+"\n"
                    text+="A:"+table.row_values(i+1)[2]+"\n"
                    text+="B:"+table.row_values(i+1)[3]+"\n"
                    text+="C:"+table.row_values(i+1)[4]+"\n"
                    text+="D:"+table.row_values(i+1)[5]+"\n"
                    text+="E:"+table.row_values(i+1)[6]+"\n"
                    print(text)


                    answer=input("Please enter an answer:")
                    if answer == table.row_values(i+1)[7]:
                        print("Congratulations,you got it!")
                        print("-------------------------------------------------")
                        print("Enter 'quit' to finish the test.")
                        break
                    else:
                        print("Your answer is wrong,the correct answer is:" + table.row_values(i+1)[7])

                        print("-------------------------------------------------")
                        print("Enter 'quit' to finish the test.")
                        break
    def write_md(self,name,title,author):
        self.title=title
        self.author=author
        path="C:\\Users\\DELL\\Desktop\\{}.md".format(name)
        md=self.gerenate_md()
        if os.path.exists(path):
            return

        with open(path,'w',encoding='utf-8') as f:
            f.write(md)



    def gerenate_md(self):
        md=""
        md += self.gerenate_header()+"\n"
        md += self.gerenate_content()+"\n"
        md += self.gerenate_footer()+"\n"
        return md

    def gerenate_header(self):
        header = ""
        header += "# **{}**".format(self.title)
        header += "\n"
        return header

    def gerenate_content(self):
        content=""
        data = self.data
        table = data.sheets()[0]
        nrows = table.nrows
        option = ["Question", "A", "B", "C", "D", "E", "Answer"]
        for i in range(1, nrows):
            content += "**{}**.".format(str(int(table.row_values(i)[0])))
            for j in range(0, 7):

                content += "**{}**:{}".format(option[j],table.row_values(i)[j+1])
                content += "\n"
            content += "\n"

        return content
    def gerenate_footer(self):
        footer = ""
        footer+="### "
        footer += "data:{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        footer += "### "

        footer += "author:{}\n".format(self.author)
        footer += "---\n"
        return footer
def main():
    version=Dissection("xjtk.xls","localhost",22,"root","","exam","utf8")
    #version.excel_test()
    #version.write_md("系解题库","系解题库","齐呈祥")
    version.download("xjtk.xls")


if __name__=="__main__":
    main()