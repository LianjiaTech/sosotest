class DomainConst(object):
    CRM = "crmDomain" #对应tb_config_http表中的配置文件中的 [HTTP]下面的crmDomain这个key  ，在HttpBase中的uri如果是对应的key，则选择对应的域名
    API = "apiDomain"