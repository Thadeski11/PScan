import socket
import argparse
from ratelimit import limits, sleep_and_retry
from scapy.all import IP, TCP, sr, L3RawSocket, conf, RandShort

global dict_ports_services_2000
dict_ports_services_2000 = {80:'http',23:'telnet',443:'https',21:'ftp',22:'ssh',25:'smtp',3389:'ms-wbt-server',110:'pop3',445:'microsoft-ds',139:'netbios-ssn',143:'imap',53:'domain',135:'msrpc',3306:'mysql',8080:'http-proxy',1723:'pptp',111:'rpcbind',995:'pop3s',993:'imaps',5900:'vnc',1025:'NFS-or-IIS',587:'submission',8888:'sun-answerbook',199:'smux',1720:'h323q931',465:'smtps',548:'afp',113:'ident',81:'hosts2-ns',6001:'X11:1',10000:'snet-sensor-mgmt',514:'shell',5060:'sip',179:'bgp',1026:'LSA-or-nterm',2000:'cisco-sccp',8443:'https-alt',8000:'http-alt',32768:'filenet-tms',554:'rtsp',26:'rsftp',1433:'ms-sql-s',49152:'unknown',2001:'dc',515:'printer',8008:'http',49154:'unknown',1027:'IIS',5666:'nrpe',646:'ldp',5000:'upnp',5631:'pcanywheredata',631:'ipp',49153:'unknown',8081:'blackice-icecap',2049:'nfs',88:'kerberos-sec',79:'finger',5800:'vnc-http',106:'pop3pw',2121:'ccproxy-ftp',1110:'nfsd-status',49155:'unknown',6000:'X11',513:'login',990:'ftps',5357:'wsdapi',427:'svrloc',49156:'unknown',543:'klogin',544:'kshell',5101:'admdog',144:'news',7:'echo',389:'ldap',8009:'ajp13',3128:'squid-http',444:'snpp',9999:'abyss',5009:'airport-admin',7070:'realserver',5190:'aol',3000:'ppp',5432:'postgresql',1900:'upnp',3986:'mapper-ws_ethd',13:'daytime',1029:'ms-lsa',9:'discard',5051:'ida-agent',6646:'unknown',49157:'unknown',1028:'unknown',873:'rsync',1755:'wms',2717:'pn-requester',4899:'radmin',9100:'jetdirect',119:'nntp',37:'time',1000:'cadlock',3001:'nessus',5001:'commplex-link',82:'xfer',10010:'rxapi',1030:'iad1',9090:'zeus-admin',2107:'msmq-mgmt',1024:'kdm',2103:'zephyr-clt',6004:'X11:4',1801:'msmq',5050:'mmcc',19:'chargen',8031:'unknown',1041:'danf-ak2',255:'unknown',1049:'td-postman',1048:'neod2',2967:'symantec-av',1053:'remote-as',3703:'adobeserver-3',1056:'vfo',1065:'syscomlan',1064:'jstel',1054:'brvread',17:'qotd',808:'ccproxy-http',3689:'rendezvous',1031:'iad2',1044:'dcutility',1071:'bsquare-voip',5901:'vnc-1',100:'newacct',9102:'jetdirect',8010:'xmpp',2869:'icslap',1039:'sbl',5120:'barracuda-bbs',4001:'newoak',9000:'cslistener',2105:'eklogin',636:'ldapssl',1038:'mtqp',2601:'zebra',1:'tcpmux',7000:'afs3-fileserver',1066:'fpo-fns',1069:'cognex-insight',625:'apple-xsrvr-admin',311:'asip-webadmin',280:'http-mgmt',254:'unknown',4000:'remoteanything',1993:'snmp-tcp-port',1761:'landesk-rc',5003:'filemaker',2002:'globe',2005:'deslogin',1998:'x25-svc-port',1032:'iad3',1050:'java-or-OTGfileshare',6112:'dtspc',3690:'svn',1521:'oracle',2161:'apc-agent',6002:'X11:2',1080:'socks',2401:'cvspserver',4045:'lockd',902:'iss-realsecure',7937:'nsrexecd',787:'qsc',1058:'nim',2383:'ms-olap4',32771:'sometimes-rpc5',1033:'netinfo',1040:'netsaint',1059:'nimreg',50000:'ibm-db2',5555:'freeciv',10001:'scp-config',1494:'citrix-ica',593:'http-rpc-epmap',2301:'compaqdiag',3:'compressnet',1:'tcpmux',3268:'globalcatLDAP',7938:'lgtomapper',1234:'hotline',1022:'exp2',1074:'warmspotMgmt',8002:'teradataordbms',1036:'nsstp',1035:'multidropper',9001:'tor-orport',1037:'ams',464:'kpasswd5',497:'retrospect',1935:'rtmp',6666:'irc',2003:'finger',6543:'mythtv',1352:'lotusnotes',24:'priv-mail',3269:'globalcatLDAPssl',1111:'lmsocialserver',407:'timbuktu',500:'isakmp',20:'ftp-data',2006:'invokator',3260:'iscsi',15000:'hydap',1218:'aeroflight-ads',1034:'zincite-a',4444:'krb524',264:'bgmp',2004:'mailbox',33:'dsp',1042:'afrog',42510:'caerpc',999:'garcon',3052:'powerchute',1023:'netvenuechat',1068:'instl_bootc',222:'rsh-spx',7100:'font-service',888:'accessbuilder',4827:'squid-htcp',1999:'tcp-id-port',563:'snews',1717:'fj-hdnet',2008:'conf',992:'telnets',32770:'sometimes-rpc3',32772:'sometimes-rpc7',7001:'afs3-callback',8082:'blackice-alerts',2007:'dectalk',740:'netcp',5550:'sdadmind',2009:'news',5801:'vnc-http-1',1043:'boinc',512:'exec',2701:'sms-rcinfo',7019:'doceri-ctl',50001:'unknown',1700:'mps-raft',4662:'edonkey',2065:'dlsrpn',2010:'search',42:'nameserver',9535:'man',2602:'ripd',3333:'dec-notes',161:'snmp',5100:'admd',5002:'rfe',2604:'ospfd',4002:'mlchat-proxy',6059:'X11:59',1047:'neod1',8192:'sophos',8193:'sophos',2702:'sms-xfer',6789:'ibm-db2-admin',9595:'pds',1051:'optima-vnet',9594:'msgsys',9593:'cba8',16993:'amt-soap-https',16992:'amt-soap-http',5226:'hp-status',5225:'hp-server',32769:'filenet-rpc',3283:'netassistant',1052:'ddt',8194:'sophos',1055:'ansyslmd',1062:'veracity',9415:'unknown',8701:'unknown',8652:'unknown',8651:'unknown',8089:'unknown',65389:'unknown',65000:'unknown',64680:'unknown',64623:'unknown',55600:'unknown',55555:'unknown',52869:'unknown',35500:'unknown',33354:'unknown',23502:'unknown',20828:'unknown',1311:'rxmon',1060:'polestar',4443:'pharos',730:'netviewdm2',731:'netviewdm3',709:'entrustmanager',1067:'instl_boots',13782:'netbackup',5902:'vnc-2',366:'odmr',9050:'tor-socks',1002:'windows-icfw',85:'mit-ml-dev',5500:'hotline',5431:'park-agent',1864:'paradym-31',1863:'msnp',8085:'unknown',51103:'unknown',49999:'unknown',45100:'unknown',10243:'unknown',49:'tacacs',3495:'seclayer-tcp',6667:'irc',90:'dnsix',475:'tcpnethaspsrv',27000:'flexlm0',1503:'imtc-mcs',6881:'bittorrent-tracker',1500:'vlsi-lm',8021:'ftp-proxy',340:'unknown',78:'vettcp',5566:'westec-connect',8088:'radan-http',2222:'EtherNetIP-1',9071:'unknown',8899:'ospf-lite',6005:'X11:5',9876:'sd',1501:'sas-3',5102:'admeng',32774:'sometimes-rpc11',32773:'sometimes-rpc9',9101:'jetdirect',5679:'activesync',163:'cmip-man',648:'rrp',146:'iso-tp0',1666:'netview-aix-6',901:'samba-swat',83:'mit-ml-dev',9207:'wap-vcal-s',8001:'vcom-tunnel',8083:'us-srv',8084:'websnp',5004:'avt-profile-1',3476:'nppmp',5214:'unknown',14238:'unknown',12345:'netbus',912:'apex-mesh',30:'unknown',2605:'bgpd',2030:'device2',6:'unknown',541:'uucp-rlogin',8007:'ajp12',3005:'deslogin',4:'unknown',1248:'hermes',2500:'rtsserv',880:'unknown',306:'unknown',4242:'vrml-multi-use',1097:'sunclustermgr',9009:'pichat',2525:'ms-v-worlds',1086:'cplscrambler-lg',1088:'cplscrambler-al',8291:'unknown',52822:'unknown',6101:'backupexec',900:'omginitialrefs',7200:'fodms',2809:'corbaloc',395:'netcp',800:'mdbs_daemon',32775:'sometimes-rpc13',12000:'cce4x',1083:'ansoft-lm-1',211:'914c-g',987:'unknown',705:'agentx',20005:'btx',711:'cisco-tdp',13783:'netbackup',6969:'acmsoda',3071:'csd-mgmt-port',5269:'xmpp-server',5222:'xmpp-client',1085:'webobjects',1046:'wfremotertm',5987:'wbem-rmi',5989:'wbem-https',5988:'wbem-http',2190:'tivoconnect',3301:'tarantool',11967:'sysinfo-sp',8600:'asterix',3766:'sitewatch-s',7627:'soap-http',8087:'simplifymedia',30000:'ndmps',9010:'sdr',7741:'scriptview',14000:'scotty-ft',3367:'satvid-datalnk',1099:'rmiregistry',1098:'rmiactivation',3031:'eppc',2718:'pn-requester2',6580:'parsec-master',15002:'onep-tls',4129:'nuauth',6901:'jetstream',3827:'netmpi',3580:'nati-svrloc',2144:'lv-ffx',9900:'iua',8181:'intermapper',3801:'ibm-mgr',1718:'h323gatedisc',2811:'gsiftp',9080:'glrpc',2135:'gris',1045:'fpitp',2399:'fmpro-fdal',3017:'event_listener',10002:'documentum',1148:'elfiq-repl',9002:'dynamid',8873:'dxspider',2875:'dxmessagebase2',9011:'d-star',5718:'dpm',8086:'d-s-n',3998:'dnx',2607:'connection',11110:'sgi-soap',4126:'ddrepl',9618:'condor',2381:'compaq-https',1096:'cnrprotocol',3300:'ceph',3351:'btrieve',1073:'bridgecontrol',8333:'bitcoin',3784:'bfd-control',5633:'beorl',15660:'bex-xr',6123:'backup-express',3211:'avsecuremgmt',1078:'avocent-proxy',5910:'cm',5911:'cpdlc',3659:'apple-sasl',3551:'apcupsd',2260:'apc-2260',2160:'apc-2160',2100:'amiganetfs',16001:'fmsascon',3325:'active-net',3323:'active-net',1104:'xrl',9968:'unknown',9503:'unknown',9502:'unknown',9485:'unknown',9290:'unknown',9220:'unknown',8994:'unknown',8649:'unknown',8222:'unknown',7911:'unknown',7625:'unknown',7106:'unknown',65129:'unknown',63331:'unknown',6156:'unknown',6129:'unknown',60020:'unknown',5962:'unknown',5961:'unknown',5960:'unknown',5959:'unknown',5925:'unknown',5877:'unknown',5825:'unknown',5810:'unknown',58080:'unknown',57294:'unknown',50800:'unknown',50006:'unknown',50003:'unknown',49160:'unknown',49159:'unknown',49158:'unknown',48080:'unknown',40193:'unknown',34573:'unknown',34572:'unknown',34571:'unknown',3404:'unknown',33899:'unknown',32782:'unknown',32781:'unknown',31038:'unknown',30718:'unknown',28201:'unknown',27715:'unknown',25734:'unknown',24800:'unknown',22939:'unknown',21571:'unknown',20221:'unknown',20031:'unknown',19842:'unknown',19801:'unknown',19101:'unknown',17988:'unknown',1783:'unknown',16018:'unknown',16016:'unknown',15003:'unknown',14442:'unknown',13456:'unknown',10629:'unknown',10628:'unknown',10626:'unknown',10621:'unknown',10617:'unknown',10616:'unknown',10566:'unknown',10025:'unknown',10024:'unknown',10012:'unknown',1169:'tripwire',5030:'surfpass',5414:'statusd',1057:'startron',6788:'smc-http',1947:'sentinelsrm',1094:'rootd',1075:'rdrmshc',1108:'ratio-adp',4003:'pxc-splr-ft',1081:'pvuniwien',1093:'proofd',4449:'privatewire',1687:'nsjtp-ctrl',1840:'netopia-vo2',1100:'mctp',1063:'kyoceranetdev',1061:'kiosk',1107:'isoipsigport-2',1106:'isoipsigport-1',9500:'ismserver',20222:'ipulse-ics',7778:'interwise',1077:'imgames',1310:'husky',2119:'gsigatekeeper',2492:'groove',1070:'gmrupdateserv',20000:'dnp',8400:'cvd',1272:'cspmlockmgr',6389:'clariion-evr01',7777:'cbt',1072:'cardax',1079:'asprovatalk',1082:'amt-esd-prot',8402:'abarsd',89:'su-mit-tg',691:'resvc',1001:'webpush',32776:'sometimes-rpc15',1999:'tcp-id-port',212:'anet',2020:'xinupageserver',6003:'X11:3',7002:'afs3-prserver',2998:'iss-realsec',50002:'iiimsf',3372:'msdtc',898:'sun-manageconsole',5510:'secureidprop',32:'unknown',2033:'glogger',4165:'altcp',3061:'cautcpd',99:'metagram',749:'kerberos-adm',425:'icad-el',5903:'vnc-3',43:'whois',5405:'pcduo',6106:'isdninfo',13722:'netbackup',6502:'netop-rc',7007:'afs3-bos',458:'appleqtc',9666:'zoomcp',8100:'xprint-server',3737:'xpanel',5298:'presence',1152:'winpoplanmess',8090:'opsmessaging',2191:'tvbus',3011:'trusted-web',1580:'tn-tl-r1',9877:'x510',5200:'targus-getdata',3851:'spectraport',3371:'satvid-datalnk',3370:'satvid-datalnk',3369:'satvid-datalnk',7402:'rtps-dd-mt',5054:'rlm-admin',3918:'pktcablemmcops',3077:'orbix-loc-ssl',7443:'oracleas-https',3493:'nut',3828:'neteh',1186:'mysql-cluster',2179:'vmrdp',1183:'llsurfup-http',19315:'keyshadow',19283:'keysrvr',3995:'iss-mgmt-ssl',5963:'indy',1124:'hpvmmcontrol',8500:'fmtp',1089:'ff-annunc',10004:'emcrmirccd',2251:'dif-port',1087:'cplscrambler-in',5280:'xmpp-bosh',3871:'avocent-adsap',3030:'arepa-cas',62078:'iphone-sync',5904:'ag-swim',9091:'xmltec-xmlmail',4111:'xgrid',1334:'writesrv',3261:'winshadow',2522:'windb',5859:'wherehoo',1247:'visionpyramid',9944:'unknown',9943:'unknown',9110:'unknown',8654:'unknown',8254:'unknown',8180:'unknown',8011:'unknown',7512:'unknown',7435:'unknown',7103:'unknown',61900:'unknown',61532:'unknown',5922:'unknown',5915:'unknown',5822:'unknown',56738:'unknown',55055:'unknown',51493:'unknown',50636:'unknown',50389:'unknown',49175:'unknown',49165:'unknown',49163:'unknown',3546:'unknown',32784:'unknown',27355:'unknown',27353:'unknown',27352:'unknown',24444:'unknown',19780:'unknown',18988:'unknown',16012:'unknown',15742:'unknown',10778:'unknown',4006:'pxc-spvr',2126:'pktcable-cops',4446:'n1-fwp',3880:'igrs',1782:'hp-hcip',1296:'dproxy',9998:'distinct32',9040:'tor-trans',32779:'sometimes-rpc21',1021:'exp1',32777:'sometimes-rpc17',2021:'servexec',32778:'sometimes-rpc19',616:'sco-sysmgr',666:'doom',700:'epp',5802:'vnc-http-2',4321:'rwhois',545:'ekshell',1524:'ingreslock',1112:'msql',49400:'compaqdiag',84:'ctf',38292:'landesk-cba',2040:'lam',32780:'sometimes-rpc23',3006:'deslogind',2111:'kx',1084:'ansoft-lm-2',1600:'issd',2048:'dls-monitor',2638:'sybase',9111:'DragonIDSConsole',6699:'napster',16080:'osxwebadmin',6547:'powerchuteplus',6007:'X11:7',1533:'virtual-places',5560:'isqlplus',2106:'ekshell',1443:'ies-lm',667:'disclose',720:'unknown',2034:'scoremgr',555:'dsf',801:'device',6025:'x11',3221:'xnm-clear-text',3826:'wormux',9200:'wap-wsp',2608:'wag-service',4279:'vrml-multi-use',7025:'vmsvc-2',11111:'vce',3527:'beserver-msg-q',1151:'unizensus',8200:'trivnet1',8300:'tmi',6689:'tsa',9878:'kca-service',10009:'swdtp-sv',8800:'sunwebadmin',5730:'unieng',2394:'ms-olap2',2393:'ms-olap1',2725:'msolap-ptp2',5061:'sip-tls',6566:'sane-port',9081:'cisco-aqos',5678:'rrac',5906:'rpas-c2',3800:'pwgpsi',4550:'gds-adppiw-db',5080:'onscreen',1201:'nucleus-sand',3168:'poweronnud',3814:'neto-dcs',1862:'mysql-cm-agent',1114:'mini-sql',6510:'mcer-port',3905:'mupdate',8383:'m2mservices',3914:'listcrt-port-2',3971:'lanrevserver',3809:'apocd',5033:'jtnetd-server',7676:'imqbrokerd',3517:'802-11-iapp',4900:'hfcs',3869:'ovsam-mgmt',9418:'git',2909:'funk-dialout',3878:'fotogcad',8042:'fs-agent',1091:'ff-sm',1090:'ff-fms',3920:'exasoftport1',6567:'esp',1138:'encrypted_admin',3945:'emcads',1175:'dossier',10003:'documentum_s',3390:'dsc',5907:'dsd',3889:'dandv-tester',1131:'caspssl',8292:'blp3',5087:'biotic',1119:'bnetgame',1117:'ardus-mtrns',4848:'appserv-http',7800:'asr',16000:'fmsas',3324:'active-net',3322:'active-net',5221:'3exmp',4445:'upnotifyp',9917:'unknown',9575:'unknown',9099:'unknown',9003:'unknown',8290:'unknown',8099:'unknown',8093:'unknown',8045:'unknown',7921:'unknown',7920:'unknown',7496:'unknown',6839:'unknown',6792:'unknown',6779:'unknown',6692:'unknown',6565:'unknown',60443:'unknown',5952:'unknown',5950:'unknown',5862:'unknown',5850:'unknown',5815:'unknown',5811:'unknown',57797:'unknown',56737:'unknown',5544:'unknown',55056:'unknown',5440:'unknown',54328:'unknown',54045:'unknown',52848:'unknown',52673:'unknown',50500:'unknown',50300:'unknown',49176:'unknown',49167:'unknown',49161:'unknown',44501:'unknown',44176:'unknown',41511:'unknown',40911:'unknown',32785:'unknown',32783:'unknown',30951:'unknown',27356:'unknown',26214:'unknown',25735:'unknown',19350:'unknown',18101:'unknown',18040:'unknown',17877:'unknown',16113:'unknown',15004:'unknown',14441:'unknown',12265:'unknown',12174:'unknown',10215:'unknown',10180:'unknown',4567:'tram',6100:'synchronet-db',4004:'pxc-roid',4005:'pxc-pin',8022:'oa-system',9898:'monkeycom',7999:'irdmi2',1271:'excw',1199:'dmidi',3003:'cgms',1122:'availant-mgr',2323:'3d-nfsd',4224:'xtell',2022:'down',617:'sco-dtmgr',777:'multiling-http',417:'onmux',714:'iris-xpcs',6346:'gnutella',981:'unknown',722:'unknown',1009:'unknown',4998:'maybe-veritas',70:'gopher',1076:'sns_credit',5999:'ncd-conf',10082:'amandaidx',765:'webster',301:'unknown',524:'ncp',668:'mecomm',2041:'interbase',6009:'X11:9',1417:'timbuktu-srv1',1434:'ms-sql-m',259:'esro-gen',44443:'coldfusion-auth',1984:'bigbrother',2068:'avocentkvm',7004:'afs3-kaserver',1007:'unknown',4343:'unicall',416:'silverplatter',2038:'objectmanager',6006:'X11:6',109:'pop2',4125:'rww',1461:'ibm_wrless_lan',9103:'jetdirect',911:'xact-backup',726:'unknown',1010:'surf',2046:'sdfunc',2035:'imsldoc',7201:'dlip',687:'asipregistry',2013:'raid-am',481:'dvs',125:'locus-map',6669:'irc',6668:'irc',903:'iss-console-mgr',1455:'esl-lm',683:'corba-iiop',1011:'unknown',2043:'isis-bcast',2047:'dls',256:'fw1-secureremote',9929:'nping-echo',5998:'ncd-diag',406:'imsp',31337:'Elite',44442:'coldfusion-auth',783:'spamassassin',843:'unknown',2042:'isis',2045:'cdfunc',4040:'yo-main',6060:'x11',6051:'x11',1145:'x9-icue',3916:'wysdmc',9443:'tungsten-https',9444:'wso2esb-console',1875:'westell-stats',7272:'watchme-7272',4252:'vrml-multi-use',4200:'vrml-multi-use',7024:'vmsvc',1556:'veritas_pbx',13724:'vnetd',1141:'mxomss',1233:'univ-appserver',8765:'ultraseek-http',1137:'trim',3963:'thrp',5938:'teamviewer',9191:'sun-as-jpda',3808:'sun-as-iiops-ca',8686:'sun-as-jmxrmi',3981:'starfish',2710:'sso-service',3852:'sse-app-config',3849:'spw-dnspreload',3944:'sops',3853:'sscan',9988:'nsesrvr',1163:'sddp',4164:'silverpeakcomm',3820:'scp',6481:'servicetags',3731:'smap',5081:'sdl-ets',40000:'safetynetp',8097:'sac',4555:'rsip',3863:'asap-tcp',1287:'routematch',4430:'rsqlserver',7744:'raqmon-pdu',1812:'radius',7913:'qo-secure',1166:'qsm-remote',1164:'qsm-proxy',1165:'qsm-gui',8019:'qbdb',10160:'qb-db-server',4658:'playsta2-app',7878:'owms',3304:'opsession-srvr',3307:'opsession-prxy',1259:'opennl-voice',1092:'obrpd',7278:'oma-dcdocbs',3872:'oem-agent',10008:'octopus',7725:'nitrogen',3410:'networklenss',1971:'netop-school',3697:'nw-license',3859:'nav-port',3514:'must-p2p',4949:'munin',4147:'vrxpservman',7900:'mevent',5353:'mdns',3931:'msr-plugin-port',8675:'msi-cps-rm',1277:'miva-mqs',3957:'mqe-broker',1213:'mpc-lifenet',2382:'ms-olap3',6600:'mshvlm',3700:'lrs-paging',3007:'lotusmtap',4080:'lorica-in',1113:'ltp-deepspace',3969:'landmarks',1132:'kvm-via-ip',1309:'jtag-server',3848:'item',7281:'itactionserver2',3907:'imoguia-port',3972:'iconp',3968:'ianywhere-dbns',1126:'hpvmmdata',5223:'hpvirtgrp',1217:'hpss-ndapi',3870:'ovsam-d-agent',3941:'homeportal-web',8293:'hiperscan-id',1719:'h323gatestat',1300:'h323hostcallsc',2099:'h2250-annex-g',6068:'gsmp',3013:'gilatskysurfer',3050:'gds_db',1174:'fnet-remote-ui',3684:'faxstfx-port',2170:'eyetv',3792:'sitewatch',1216:'etebac5',5151:'esri_sde',7123:'snif',7080:'empowerid',22222:'easyengine',4143:'oidsr',5868:'diameters',8889:'ddi-tcp-2',12006:'dbisamserver2',1121:'rmpp',3119:'d2000kernel',8015:'cfg-cloud',10023:'cefd-vmp',3824:'acp-policy',1154:'resacommunity',20002:'commtact-http',3888:'ciphire-serv',4009:'chimera-hwm',5063:'csrpc',3376:'cdbroker',1185:'catchpole',1198:'cajo-discovery',1192:'caids-sensor',1972:'intersys-cache',1130:'casp',1149:'bvtsonar',4096:'bre',6500:'boks',8294:'blp4',3990:'bv-is',3993:'bv-agent',8016:'ads-s',5242:'attune',3846:'an-pcp',3929:'smauth-port',1187:'alias',5074:'alesquery',5909:'agma',8766:'amcs',5905:'asmgcs',1102:'adobeserver-1',2800:'acc-raid',9941:'unknown',9914:'unknown',9815:'unknown',9673:'unknown',9643:'unknown',9621:'unknown',9501:'unknown',9409:'unknown',9198:'unknown',9197:'unknown',9098:'unknown',8996:'unknown',8987:'unknown',8877:'unknown',8676:'unknown',8648:'unknown',8540:'unknown',8481:'unknown',8385:'unknown',8189:'unknown',8098:'unknown',8095:'unknown',8050:'unknown',7929:'unknown',7770:'unknown',7749:'unknown',7438:'unknown',7241:'unknown',7051:'unknown',7050:'unknown',6896:'unknown',6732:'unknown',6711:'unknown',65310:'unknown',6520:'unknown',6504:'unknown',6247:'unknown',6203:'unknown',61613:'unknown',60642:'unknown',60146:'unknown',60123:'unknown',5981:'unknown',5940:'unknown',59202:'unknown',59201:'unknown',59200:'unknown',5918:'unknown',5914:'unknown',59110:'unknown',5899:'unknown',58838:'unknown',5869:'unknown',58632:'unknown',58630:'unknown',5823:'unknown',5818:'unknown',5812:'unknown',5807:'unknown',58002:'unknown',58001:'unknown',57665:'unknown',55576:'unknown',55020:'unknown',53535:'unknown',5339:'unknown',53314:'unknown',53313:'unknown',53211:'unknown',52853:'unknown',52851:'unknown',52850:'unknown',52849:'unknown',52847:'unknown',5279:'unknown',52735:'unknown',52710:'unknown',52660:'unknown',5212:'unknown',51413:'unknown',51191:'unknown',5040:'unknown',50050:'unknown',49401:'unknown',49236:'unknown',49195:'unknown',49186:'unknown',49171:'unknown',49168:'unknown',49164:'unknown',4875:'unknown',47544:'unknown',46996:'unknown',46200:'unknown',44709:'unknown',41523:'unknown',41064:'unknown',40811:'unknown',3994:'unknown',39659:'unknown',39376:'unknown',39136:'unknown',38188:'unknown',38185:'unknown',37839:'unknown',35513:'unknown',33554:'unknown',33453:'unknown',32835:'unknown',32822:'unknown',32816:'unknown',32803:'unknown',32792:'unknown',32791:'unknown',30704:'unknown',30005:'unknown',29831:'unknown',29672:'unknown',28211:'unknown',27357:'unknown',26470:'unknown',23796:'unknown',23052:'unknown',2196:'unknown',21792:'unknown',19900:'unknown',18264:'unknown',18018:'unknown',17595:'unknown',16851:'unknown',16800:'unknown',16705:'unknown',15402:'unknown',15001:'unknown',12452:'unknown',12380:'unknown',12262:'unknown',12215:'unknown',12059:'unknown',12021:'unknown',10873:'unknown',10058:'unknown',10034:'unknown',10022:'unknown',10011:'unknown',2910:'tdaccess',1594:'sixtrak',1658:'sixnetudr',1583:'simbaexpress',3162:'sflm',2920:'roboeda',26000:'quake',2366:'qip-login',4600:'piranha1',1688:'nsjtp-data',1322:'novation',2557:'nicetec-mgmt',1095:'nicelink',1839:'netopia-vo1',2288:'netml',1123:'murray',5968:'mppolicy-v5',9600:'micromuse-ncpw',1244:'isbconference1',1641:'invision',2200:'ici',1105:'ftranhc',6550:'fg-sysupdate',5501:'fcp-addr-srvr2',1328:'ewall',2968:'enpp',1805:'enl-name',1914:'elm-momentum',1974:'drp',31727:'diagd',3400:'csms2',1301:'ci3-software-1',1147:'capioverlan',1721:'caicci',1236:'bvcontrol',2501:'rtsclient',2012:'ttyinfo',6222:'radmind',1220:'quicktime',1109:'kpop',1347:'bbn-mmc',502:'mbap',701:'lmp',2232:'ivs-video',2241:'ivsd',4559:'hylafax',710:'entrust-ash',10005:'stel',5680:'canna',623:'oob-ws-http',913:'apex-edge',1103:'xaudio',780:'wpgs',930:'unknown',803:'unknown',725:'unknown',639:'msdp',540:'uucp',102:'iso-tsap',5010:'telelpathstart',1222:'nerv',953:'rndc',8118:'privoxy',9992:'issc',1270:'ssserver',27:'nsw-fe',123:'ntp',86:'mfcobol',447:'ddm-dfm',1158:'lsnr',442:'cvc_hostd',18000:'biimenu',419:'ariel1',931:'unknown',874:'unknown',856:'unknown',250:'unknown',475:'tcpnethaspsrv',2044:'rimsl',441:'decvms-sysmgt',210:'z39.50',6008:'X11:8',7003:'afs3-vlserver',5803:'vnc-http-3',1008:'ufsd',556:'remotefs',6103:'RETS-or-BackupExec',829:'pkix-3-ca-ra',3299:'saprouter',55:'isi-gl',713:'iris-xpc',1550:'3m-image-lm',709:'entrustmanager',2628:'dict',223:'cdc',3025:'slnp',87:'priv-term-l',57:'priv-term',10083:'amidxtape',5520:'sdlog',980:'unknown',251:'unknown',1013:'unknown',9152:'ms-sql2000',1212:'lupa',2433:'codasrv-se',1516:'vpad',333:'texar',2011:'raid-cc',748:'ris-cm',1350:'editbench',1526:'pdap-np',7010:'ups-onlinet',1241:'nessus',127:'locus-con',157:'knet-cmp',220:'imap3',1351:'equationbuilder',2067:'dlswpn',684:'corba-iiop-ssl',77:'priv-rje',4333:'msql',674:'acap',943:'unknown',904:'unknown',840:'unknown',825:'unknown',792:'unknown',732:'unknown',1020:'unknown',1006:'unknown',657:'rmc',557:'openvms-sysipc',610:'npmp-local',1547:'laplink',523:'ibm-db2',996:'xtreelic',2025:'ellpack',602:'xmlrpc-beep',3456:'vat',862:'twamp-control',600:'ipcserver',2903:'extensisportfolio',257:'fw1-mc-fwmodule',1522:'rna-lm',1353:'relief',6662:'radmind',998:'busboy',660:'mac-srvr-admin',729:'netviewdm1',730:'netviewdm2',731:'netviewdm3',782:'hp-managed-node',1357:'pegboard',3632:'distccd',3399:'sapeps',6050:'arcserve',2201:'ats',971:'unknown',969:'unknown',905:'unknown',846:'unknown',839:'unknown',823:'unknown',822:'unknown',795:'unknown',790:'unknown',778:'unknown',757:'unknown',659:'unknown',225:'unknown',1015:'unknown',1014:'unknown',1012:'unknown',655:'tinc',786:'concert',6017:'xmail-ctrl',6670:'irc',690:'vatp',388:'unidata-ldm',44334:'tinyfw',754:'krb_prop',5011:'telelpathattack',98:'linuxconf',411:'rmt',1525:'orasrv',3999:'remoteanything',740:'netcp',12346:'netbus',802:'mbap-s',1337:'waste',1127:'supfiledbg',2112:'kip',1414:'ibm-mqseries',2600:'zebrasrv',621:'escp-ip',606:'urm',59:'priv-file',928:'unknown',924:'unknown',922:'unknown',921:'unknown',918:'unknown',878:'unknown',864:'unknown',859:'unknown',806:'unknown',805:'unknown',728:'unknown',252:'unknown',1005:'unknown',1004:'unknown',641:'repcmd',758:'nlogin',669:'meregister',38037:'landesk-cba',715:'iris-lwz',1413:'innosys-acl',2104:'zephyr-hm',1229:'zented',3817:'tapeware',6063:'x11',6062:'x11',6055:'x11',6052:'x11',6030:'x11',6021:'x11',6015:'x11',6010:'x11',3220:'xnm-ssl',6115:'xic',3940:'xecp-node',2340:'wrs_registry',8006:'wpl-analytics',4141:'oirtgsvc',3810:'wlanauth',1565:'winddlb',3511:'webmail-2',5986:'wsmans',5985:'wsman',33000:'wg-endpt-comms',2723:'watchdog-nt',9202:'wap-wsp-s',4036:'wap-push-https',4035:'wap-push-http',2312:'wanscaler',3652:'vxcrnbuport',3280:'vs-server',4243:'vrml-multi-use',4298:'vrml-multi-use',4297:'vrml-multi-use',4294:'vrml-multi-use',4262:'vrml-multi-use',4234:'vrml-multi-use',4220:'vrml-multi-use',4206:'vrml-multi-use',22555:'vocaltec-wconf',9300:'vrace',7121:'virprot-lm',1927:'videte-cipc',4433:'vop',5070:'vtsas',2148:'veritas-ucl',1168:'vchat',9979:'visweather',7998:'usicontentpush',4414:'updog',1823:'unisys-lm',3653:'tsp',1223:'tgp',8201:'trivnet2',4876:'tritium-can',3240:'triomotion',2644:'travsoft-ipx-t',4020:'trap',2436:'topx',3906:'topovista-data',4375:'tolteces',4024:'tnp1-port',5581:'tmosms1',5580:'tmosms0',9694:'client-wakeup',6251:'tl1-raw-ssl',7345:'swx',7325:'swx',7320:'swx',7300:'swx',3121:'pcmk-remote',5473:'apsolab-tags',5475:'apsolab-data',3600:'trap-daemon',3943:'tig',4912:'lutap',2142:'tdmoip',1976:'tcoregagent',1975:'tcoflashagent',5202:'targus-getdata2',5201:'targus-getdata1',4016:'talarian-mcast2',5111:'taep-as-svc',9911:'sype-transport',10006:'netapp-sync',3923:'symb-sb-port',3930:'syam-webserver',1221:'sweetware-apps',2973:'svnetworks',3909:'surfcontrolcpa',5814:'spt-automation',14001:'sua',3080:'stm_pproc',4158:'stat-cc',3526:'starquiz-port',1911:'mtp',5066:'stanag-5066',2711:'sso-control',2187:'ssmc',3788:'isrp-port',3796:'spw-dialer',3922:'sor-update',2292:'mib-streaming',16161:'sun-sea-port',3102:'sl-mon',4881:'socp-t',3979:'smwan',3670:'smile',4174:'smcluster',3483:'slim-devices',2631:'sitaradir',1750:'sslp',3897:'sdo-ssh',7500:'silhouette',5553:'sgi-eventmond',5554:'sgi-esphttp',9875:'sapv1',4570:'deploymentmap',3860:'sasp',3712:'sentinel-ent',8052:'senomix01',2083:'radsec',8883:'secure-mqtt',2271:'mmcals',4606:'sixid',1208:'seagull-ais',3319:'sdt-lmd',3935:'sdp-portmapper',3430:'ssdispatch',1215:'scanstat-1',3962:'sbi-agent',3368:'satvid-datalnk',3964:'sasggprs',1128:'saphostctrl',5557:'farenet',4010:'samsung-unidex',9400:'sec-t4net-srv',1605:'slp',3291:'sah-lm',7400:'rtps-discovery',5005:'avt-profile-2',1699:'rsvp-encap-2',1195:'rsf-1',5053:'rlm',3813:'rap-ip',1712:'registrar',3002:'exlm-agent',3765:'rtraceroute',3806:'wsmlb',43000:'recvr-rc',2371:'worldwire',3532:'raven-rmp',3799:'radius-dynauth',3790:'quickbooksrds',3599:'quasar-server',3850:'qtms-bootstrap',4355:'qsnet-workst',4358:'qsnet-nucl',4357:'qsnet-cond',4356:'qsnet-assist',5433:'pyrrho',3928:'netboot-pxe',4713:'pulseaudio',4374:'psi-ptt',3961:'proaxess',9022:'paragent',3911:'prnstatus',3396:'printer_agent',7628:'zen-pawn',3200:'tick-port',1753:'predatar-comms',3967:'ppsms',2505:'ppcontrol',5133:'nbt-pc',3658:'ps-ams',8471:'pim-port',1314:'pdps',2558:'pclemultimedia',6161:'patrol-ism',4025:'partimage',3089:'ptk-alink',9021:'panagolin-ident',30001:'pago-services1',8472:'otv',5014:'onpsocket',9990:'osm-appsrvr',1159:'oracle-oms',1157:'iascontrol',1308:'odsi',5723:'omhs',3443:'ov-nnm-websrv',4161:'omscontact',1135:'omnivision',9211:'oma-mlp-s',9210:'oma-mlp',4090:'omasgport',7789:'office-tools',6619:'odette-ftps',9628:'odbcpathway',12121:'nupaper-ss',4454:'nssagentmgr',3680:'npds-tracker',3167:'nowcontact',3902:'nimaux',3901:'nimsh',3890:'ndsconnect',3842:'nhci',16900:'newbay-snc-mc',4700:'netxms-agent',4687:'nst',8980:'nod-provider',1196:'netmagic',4407:'nacagent',3520:'galileolog',3812:'neto-wol-server',5012:'nsp',10115:'netiq-endpt',1615:'netbill-auth',2902:'netaspi',4118:'netscript',2706:'ncdmirroring',2095:'nbx-ser',2096:'nbx-dir',3363:'nati-vi-server',5137:'ctsd',3795:'myblast',8005:'mxi',10007:'mvs-capacity',3515:'must-backplane',8003:'mcreport',3847:'msfw-control',3503:'lsp-ping',5252:'movaz-ssc',27017:'mongod',2197:'mnp-exchange',4120:'minirem',1180:'mc-client',5722:'msdfsr',1134:'aplx',1883:'mqtt',1249:'mesavistaco',3311:'mcns-tel-ret',3837:'mkm-discovery',2804:'dvr-esm',4558:'mtcevrunqman',4190:'sieve',2463:'lsi-raid-mgmt',1204:'ssslog-mgr',4056:'lms',1184:'llsurfup-https',19333:'litecoin',9333:'litecoin',3913:'listcrt-port',3672:'lispworks-orb',4342:'lisp-cons',4877:'lmcs',3586:'emprise-lsc',8282:'libelle',1861:'lecroy-vicp',1752:'lofr-lm',9592:'ldgateway',1701:'l2f',6085:'konspire2b',2081:'kme-trap-port',4058:'kingfisher',2115:'kdm',8900:'jmb-cds1',4328:'jaxer-manager',2958:'jmact6',2957:'jmact5',7071:'iwg1',3899:'itv-control',2531:'ito-e-gui',2691:'itinternet',5052:'ita-manager',1638:'ismc',3419:'softaudit',2551:'isg-uda-server',5908:'ipsma',4029:'ip-qsig',3603:'int-rcv-cntrl',1336:'ischat',2082:'infowave',1143:'imyx',3602:'infiniswitchcl',1176:'indigo-server',4100:'igo-incognito',3486:'ifsf-hb-port',6077:'iconstructsrv',4800:'iims',2062:'icg-swp',1918:'can-nds',12001:'entextnetwk',12002:'entexthigh',9084:'aurora',7072:'iba-cfg',1156:'iascontrol-oms',2313:'iapp',3952:'i3-sessionmgr',4999:'hfcs-manager',5023:'htuilsrv',2069:'event-port',28017:'mongod',27019:'mongod',27018:'mongod',3439:'hri-port',6324:'hrd-ncs',1188:'hp-webadmin',1125:'hpvmmagent',3908:'hppronetman',7501:'ovbus',8232:'hncp-dtls-port',1722:'hks-lm',2988:'hippad',10500:'hip-nat-t',1136:'hhb-gateway',1162:'health-trap',10020:'abb-hw',22128:'gsidcap',1211:'groove-dpp',3530:'gf',12009:'ghvpn',9005:'golem',3057:'goahead-fldup',3956:'gvcp',4325:'geognosisman',1191:'gpfs',3519:'nvmsgd',5235:'galaxy-network',1144:'fuscript',4745:'fmp',1901:'fjicl-tep-a',1807:'fhsp',2425:'fjitsuappmgr',3210:'flamenco-proxy',32767:'filenet-powsrm',5015:'fmwp',5013:'fmpro-v6',3622:'ff-lr-port',4039:'fazzt-admin',10101:'ezmeeting-2',5233:'enfs',5152:'sde-discovery',3983:'eisp',3982:'eis',9616:'erunbook_agent',4369:'epmd',3728:'e-woa',3621:'ep-nsp',2291:'eapsp',5114:'ev-services',7101:'elcn',1315:'els',2087:'eli',5234:'eenet',1635:'edb-server1',3263:'ecolor-imager',4121:'e-builder',4602:'mtsserver',2224:'efi-mg',3949:'drip',9131:'dddp',3310:'dyna-access',3937:'dvbservdsc',2253:'dtv-chan-req',3882:'msdts1',3831:'dvapps',2376:'docker',2375:'docker',3876:'dl_agent',3362:'dj-ilm',3663:'dtp',3334:'directv-web',47624:'directplaysrvr',1825:'direcpc-video',3868:'diameter',4302:'d-data-control',5721:'dtpt',1279:'dellwebadmin-2',2606:'netmon',1173:'d-cinema-rrp',22125:'dcap',17500:'db-lsp',12005:'dbisamserver1',6113:'dayliteserver',1973:'dlsrap',3793:'dcsoftware',3637:'scservp',8954:'cumulus-admin',3742:'cst-port',9667:'xmms2',41795:'crestron-ctp',41794:'crestron-cip',4300:'corelccam',8445:'copy',12865:'netperf',3365:'contentserver',4665:'contclientms',3190:'csvr-proxy',3577:'config-port',3823:'acp-conduit',2261:'comotionmaster',2262:'comotionback',2812:'atmtcp',1190:'commlinx-avl',22350:'CodeMeter',3374:'cluster-disc',4135:'cl-db-attach',2598:'citriximaclient',2567:'clp',1167:'cisco-ipsla',8470:'cisco-avp',10443:'cirrossp',8116:'cp-cluster',3830:'cernsysmgmtagt',8880:'cddbp-alt',2734:'ccs-software',3505:'ccmcomm',3388:'cbserver',3669:'casanswmgmt',1871:'canocentral0',8025:'ca-audit-da',1958:'dxadmind',3681:'bts-x73',3014:'broker_service',8999:'bctp',4415:'brcd-vr-req',3414:'wip-port',4101:'brlp-0',6503:'boks_clntd',9700:'board-roar',3683:'bmc-ea',1150:'blaze',18333:'bitcoin',4376:'bip',3991:'bv-smcsrv',3989:'bv-queryengine',3992:'bv-ds',2302:'binderysupport',3415:'bcinameservice',1179:'b2n',3946:'backupedge',2203:'b2-runtime',4192:'azeti',4418:'axysbridge',2712:'aocp',25565:'minecraft',4065:'avanti_cdp',5820:'autopassdaemon',3915:'agcat',2080:'autodesk-nlm',3103:'autocuesmi',2265:'apx500api-2',8202:'aesop',2304:'attachmate-uts',8060:'aero',4119:'assuria-slm',4401:'ds-srvr',1560:'asci-val',3904:'omnilink-port',4534:'armagetronad',1835:'ardusmul',1116:'ardus-cntl',8023:'arca-api',8474:'noteshare',3879:'appss-lm',4087:'applusservice',4112:'apple-vpns-rp',6350:'adap',9950:'apc-9950',3506:'apc-3506',3948:'apdap',3825:'ffserver',2325:'ansysli',1800:'ansys-lm',1153:'c1222-acse',6379:'redis',3839:'amx-rms',5672:'amqp',4689:'altovacentral',47806:'ap',5912:'fis',3975:'airshot',3980:'acms',4113:'aipn-reg',2847:'aimpp-port-req',2070:'ah-esp-encap',3425:'agps-port',6628:'afesc-mc',3997:'agentsease-db',3513:'arcpd',3656:'abatjss',2335:'ace-proxy',1182:'accelenet',1954:'abr-api',3996:'abcsoftware',4599:'a17-an-an',2391:'3com-net-mgmt',3479:'twrpc',5021:'zenginkyo-2',5020:'zenginkyo-1',1558:'xingmpeg',1924:'xiip',4545:'worldscores',2991:'wkstn-mon',6065:'winpharaoh',1290:'winjaserver',1559:'web2host',1317:'vrts-ipcserver',5423:'virtualuser',1707:'vdmplay',5055:'unot',9975:'unknown',9971:'unknown',9919:'unknown',9915:'unknown',9912:'unknown',9910:'unknown',9908:'unknown',9901:'unknown',9844:'unknown',9830:'unknown',9826:'unknown',9825:'unknown',9823:'unknown',9814:'unknown',9812:'unknown',9777:'unknown',9745:'unknown',9683:'unknown',9680:'unknown',9679:'unknown',9674:'unknown',9665:'unknown',9661:'unknown',9654:'unknown',9648:'unknown',9620:'unknown',9619:'unknown',9613:'unknown',9583:'unknown',9527:'unknown',9513:'unknown',9493:'unknown',9478:'unknown',9464:'unknown',9454:'unknown',9364:'unknown'}

parser = argparse.ArgumentParser(prog="PScan", description="Port scanning")
parser.add_argument("--type", help='''Tipo de scan:
[SYN] Stealth scan
''')
parser.add_argument("--host", help="Passar o host teste")
parser.add_argument("--time", help="Req por segundo")
args = parser.parse_args()

@sleep_and_retry
@limits(calls=int(args.time), period=1)
def SYNscan(host, porta):
	conf.L3socket = L3RawSocket
	conf.verb = 0

	pacote_ip = IP(dst=host)
	pacote_tcp = TCP(
		dport=porta, 
		sport=RandShort(), 
		flags="S", 
		seq=1000, 
		options=[("MSS",1460),("NOP",None),("WScale",7)]
	)

	pkg, unpkg = sr(pacote_ip/pacote_tcp, timeout=0.1)

	porta_tcp = f"{porta}/tcp"
	status_open = "open"
	status_closed = "closed"

	if pkg:
		for snd, rcv in pkg:
			if rcv.haslayer(TCP):
				if rcv[TCP].flags == 0x012:
					print(f"{porta_tcp:<10} {dict_ports_services_2000[porta]:<10} {status_open:<10}")


@sleep_and_retry
@limits(calls=int(args.time), period=1)
def port_check(host, porta):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(0.1)
	porta_tcp = f"{porta}/tcp"
	status_open = "open"
	status_closed = "closed"
	if s.connect_ex((host, porta)) == 0:
		print(f"{porta_tcp:<10} {dict_ports_services_2000[porta]:<10} {status_open:<10}")
	elif s.connect_ex((host, porta)) == 111:
		print(f"{porta_tcp:<10} {dict_ports_services_2000[porta]:<10} {status_closed:<10}")


	s.close()

def get_ip(host):
	s = socket.getaddrinfo(host, None, socket.AF_INET)
	return s[2][4][0]

addr = get_ip(args.host)

print("PORT       SERVICE    STATE")
if args.type == None:	
	for porta in dict_ports_services_2000:
		port_check(addr, porta)
elif args.type == "SYN":
	for porta in dict_ports_services_2000:
		SYNscan(addr, porta)
