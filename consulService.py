import consul
import pymysql
import time


##TABLENAME
tbname='serviceTable'


##create db connect
connection = pymysql.connect(host="127.0.0.1",port=3306,user='root',
                             password='root',
                             db='consul',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

##init length of table
with connection.cursor() as cursor:
    sql = 'select count(*) from {}'.format(tbname)
    tblength =cursor.execute(sql)
    connection.commit()


##create consul object
c = consul.Consul()


while(1):
    #judge if have new service
    result = c.agent.services()
    servicemap = {}

    for i in result.values():
        servicemap[i.get("Service")] = i.get("Address")

        print(27)
    if (len(servicemap)) > tblength:


        with connection.cursor() as cursor:
            for i in servicemap.items():
                sql = "DELETE FROM {}".format(tbname)
                cursor.execute(sql)
                connection.commit()


        print(29)
        tblength = len(servicemap)
        with connection.cursor() as cursor:
            for i in servicemap.items():
                sql = "INSERT INTO {}(name,ip,flag) VALUES(%s,%s,%s)".format(tbname)
                cursor.execute(sql, (i[0], i[1], 1))
                connection.commit()



    # update helth service
    with connection.cursor() as cursor:
        sql = "UPDATE {} SET flag=1 where flag=0".format(tbname)
        cursor.execute(sql)
        connection.commit()

    print(11)
    serviceCheck = c.agent.checks()
    statemap = {}

    ##get fail service information
    for v in serviceCheck.values():
        if v.get("Status") != "passing":
            statemap[v.get("ServiceName")]=v.get("Status")

    ##update fail service
    if len(statemap.keys()) > 0:
            for k in statemap.keys():
                with connection.cursor() as cursor:
                    sql = "UPDATE {} SET flag=0 where name=(%s)".format(tbname)
                    cursor.execute(sql, k)
                    connection.commit()





    ##time interval
    time.sleep(5)








#json load agentservices





