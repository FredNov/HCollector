from PySide import QtCore, QtGui
import hou, os, shutil, re, glob, datetime, zipfile

class HCollector (QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(295, 193)

        main = QtGui.QVBoxLayout()
        fileLayout = QtGui.QHBoxLayout()
        geoLayout = QtGui.QHBoxLayout()
        imgLayout = QtGui.QHBoxLayout()
        dopLayout = QtGui.QHBoxLayout()
        customLayout = QtGui.QHBoxLayout()
        searchLay = QtGui.QHBoxLayout()
        checkLay = QtGui.QHBoxLayout()
        collectlay = QtGui.QVBoxLayout()

        self.grpB = QtGui.QGroupBox()
        self.grpB1= QtGui.QGroupBox()
        self.grpB2 = QtGui.QGroupBox()
        self.grpB3 = QtGui.QGroupBox()
        self.grpB4 = QtGui.QGroupBox()
  
        self.chFile = QtGui.QCheckBox('HipFile:')
        self.chGeo = QtGui.QCheckBox('Geometry:')
        self.chImg = QtGui.QCheckBox('Images:')
        self.chDop = QtGui.QCheckBox('Dop/Simulation:')
        self.chCustom = QtGui.QCheckBox('Custom:')
        self.ch_search = QtGui.QCheckBox('Search files:')
        self.chupd = QtGui.QCheckBox('Replace Old Files')
        self.charch = QtGui.QCheckBox('Create ZIP Archive')

        self.ln_file = QtGui.QLineEdit()
        self.ln_geo = QtGui.QLineEdit()
        self.ln_img = QtGui.QLineEdit()
        self.ln_dop = QtGui.QLineEdit()
        self.ln_attr = QtGui.QLineEdit()
        self.ln_customPath = QtGui.QLineEdit()
        self.ln_search = QtGui.QLineEdit() 
     
        self.btn_B_file = QtGui.QToolButton()   
        self.btn_B_geo = QtGui.QToolButton()
        self.btn_B_img = QtGui.QToolButton()
        self.btn_B_dop = QtGui.QToolButton()
        self.btn_B_custom = QtGui.QToolButton()
        self.btn_B_search = QtGui.QToolButton()
        self.btn_collect = QtGui.QPushButton()
        self.btn_check = QtGui.QPushButton()
        
        self.charch.setChecked(0)
        self.chFile.setChecked(0)
        self.chGeo.setChecked(1)
        self.chImg.setChecked(1)
        self.chDop.setChecked(1)
        self.chCustom.setChecked(0)
        self.ch_search.setChecked(0)
        
        hip=os.path.normcase(os.path.normpath(hou.getenv('HIP')))
        self.ln_file.setText(hip)
        self.ln_geo.setText(hip+'\\geometry')
        self.ln_img.setText(hip+'\\textures')
        self.ln_dop.setText(hip+'\\dop')
        self.ln_attr.setText("Type attribute name here")
        self.ln_customPath.setText(hip+'\\other')
        self.ln_search.setText('Parent directoty to search for lost files')
        
        fileLayout.addWidget(self.chFile)
        fileLayout.addWidget(self.ln_file)
        fileLayout.addWidget(self.btn_B_file)
        geoLayout.addWidget(self.chGeo)
        geoLayout.addWidget(self.ln_geo)
        geoLayout.addWidget(self.btn_B_geo)
        imgLayout.addWidget(self.chImg)
        imgLayout.addWidget(self.ln_img)
        imgLayout.addWidget(self.btn_B_img)
        dopLayout.addWidget(self.chDop)
        dopLayout.addWidget(self.ln_dop)
        dopLayout.addWidget(self.btn_B_dop)
        collectlay.addLayout(fileLayout)
        collectlay.addLayout(geoLayout)
        collectlay.addLayout(imgLayout)
        collectlay.addLayout(dopLayout)
        self.grpB.setLayout(collectlay)
        main.addWidget(self.grpB)

        customLayout.addWidget(self.chCustom)
        customLayout.addWidget(self.ln_attr)
        customLayout.addWidget(self.ln_customPath)
        customLayout.addWidget(self.btn_B_custom)
        self.grpB2.setLayout(customLayout)     
        main.addWidget(self.grpB2)

        searchLay.addWidget(self.ch_search)
        searchLay.addWidget(self.ln_search)
        searchLay.addWidget(self.btn_B_search)
        self.grpB4.setLayout(searchLay) 
        main.addWidget(self.grpB4)

        checkLay.addWidget(self.chupd)
        checkLay.addWidget(self.charch)

        self.grpB3.setLayout(checkLay)     
        main.addWidget(self.grpB3)
        
        main.addWidget(self.btn_collect)
        main.addWidget(self.btn_check)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        main.addItem(spacerItem)

        self.setWindowTitle("Form")
        self.btn_B_file.setText("...")
        self.btn_B_geo.setText("...")
        self.btn_B_img.setText("...")
        self.btn_B_dop.setText("...")
        self.btn_B_custom.setText("...")
        self.btn_B_search.setText("...")
        self.btn_collect.setText("Collect")
        self.btn_check.setText("Check external links / FIX absolute paths ")

        ###
        self.setLayout(main)
        self.setProperty("houdiniStyle", True)

        self.btn_B_file.clicked.connect(self.setFilePath)
        self.btn_B_geo.clicked.connect(self.setFilePath1)
        self.btn_B_img.clicked.connect(self.setFilePath2)
        self.btn_B_dop.clicked.connect(self.setFilePath3)
        self.btn_B_custom.clicked.connect(self.setFilePath4)
        self.btn_B_search.clicked.connect(self.setFilePath6)
        self.btn_collect.clicked.connect(self.collectFiles)
        self.btn_check.clicked.connect(self.checkLinks)
        self.chFile.clicked.connect(self.updateUI)
        self.chGeo.clicked.connect(self.updateUI)
        self.chImg.clicked.connect(self.updateUI)
        self.chDop.clicked.connect(self.updateUI)
        self.chCustom.clicked.connect(self.updateUI)
        self.ch_search.clicked.connect(self.updateUI)

        self.updateUI()


    def updateUI(self):
        
        if self.chFile.isChecked():
            self.ln_file.setDisabled(0)
            self.btn_B_file.setDisabled(0)
            self.ln_geo.setText(self.ln_file.text()+'\\geometry')
            self.ln_img.setText(self.ln_file.text()+'\\textures')
            self.ln_dop.setText(self.ln_file.text()+'\\dop')
            self.ln_customPath.setText(self.ln_file.text()+'\\other')
        else:
            hip=os.path.normcase(os.path.normpath(hou.getenv('HIP')))
            self.ln_file.setDisabled(1)
            self.btn_B_file .setDisabled(1)
            self.ln_file.setText(hip)
            self.ln_geo.setText(hip+'\\geometry')
            self.ln_img.setText(hip+'\\textures')
            self.ln_dop.setText(hip+'\\dop')
            self.ln_customPath.setText(hip+'\\other')

        if self.chGeo.isChecked():
            self.ln_geo.setDisabled(0)
            self.btn_B_geo.setDisabled(0)
        else:
            self.ln_geo.setDisabled(1)
            self.btn_B_geo.setDisabled(1)
        if self.chImg.isChecked():
            self.ln_img.setDisabled(0)
            self.btn_B_img.setDisabled(0)
        else:
            self.ln_img.setDisabled(1)
            self.btn_B_img.setDisabled(1)
        if self.chDop.isChecked():
            self.ln_dop.setDisabled(0)
            self.btn_B_dop.setDisabled(0)
        else:
            self.ln_dop.setDisabled(1)
            self.btn_B_dop.setDisabled(1)
        if self.chCustom.isChecked():
            self.ln_attr.setDisabled(0)
            self.ln_customPath.setDisabled(0)
            self.btn_B_custom.setDisabled(0)
        else:
            self.ln_attr.setDisabled(1)
            self.ln_customPath.setDisabled(1)
            self.btn_B_custom.setDisabled(1)
        if self.ch_search.isChecked():
            self.ln_search.setDisabled(0)
            self.btn_B_search.setDisabled(0)
        else:
            self.ln_search.setDisabled(1)
            self.btn_B_search.setDisabled(1)

    def checkExceptions(self,param):
        pth=param.eval()
        add=0
        exceptNames= ['default.bgeo','defcam.bgeo','pointlight.bgeo','defgeo.bgeo','./sdf0000.simdata']
        if pth!='' and len(param.keyframes())==0 and not param.isLocked() and not param.isDisabled() and not param.isHidden():
            pth=param.unexpandedString()
            add=1
            for ex in exceptNames:
                if pth.find(ex)==0 :
                    add=0
                k=pth.split('/')
                if k[len(k)-1].find(ex)==0 :
                    add=0
        return add

    def collectNodesByType(self,typ):
        nodesUnfiltered=[]
        nodes=[]
        if typ=='geo':
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Sop))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Rop))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Obj))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ObjBone))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ObjCamera))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ObjFog))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ObjGeometry))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ObjGeometryOrFog))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ObjLight))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ObjMuscle))
        elif typ=='img':
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Cop))      
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Shop))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopAtmosphere))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopDisplacement))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopImage3D))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopInterior))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopLight))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopLightShadow))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopMaterial))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopPhoton))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopProperties))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.ShopSurface))
        elif typ=='dop':
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Dop))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Pop))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Popnet))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Chop))
            nodesUnfiltered.append(hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Chopnet))
        flattened = []
        for sub in nodesUnfiltered:
            for val in sub:
                flattened.append(val)
        for node in flattened:
            if not node.isInsideLockedHDA():
                nodes.append(node) 
        return nodes 

    def collectParams(self,nodes):
        params=[] 
        for n in nodes:
           for arg_parm in n.globParms('*file* *out* *File*'):
               if arg_parm.parmTemplate().dataType()==hou.parmData.String:
                   if self.checkExceptions(arg_parm)!=0:
                       params.append(arg_parm)     
        return params

    def convToHip(self, pth):
        pth=os.path.normpath(os.path.normcase(pth))
        if self.chFile.isChecked():
            pth=pth.replace(self.ln_file.text(),'$HIP')
        else:
            pth=pth.replace(os.path.normpath(os.path.normcase(hou.getenv('HIP'))),'$HIP')
        pth=pth.replace('\\','/')

        if hou.getenv('JOB'):
            if os.path.exists(hou.getenv('JOB')):
                pth=pth.replace(hou.getenv('JOB'),'$JOB')
        return pth

    def convToOS(self, pth):
        pth=pth.replace('$HIP',hou.getenv('HIP'))   
        if hou.getenv('JOB'):
            if os.path.exists(hou.getenv('JOB')):
                pth=pth.replace('$JOB',hou.getenv('JOB'))
        return os.path.normcase(pth)

    def correctWrongExpr(self,parm):
        global report
        global ecount
        path=parm.eval() 
        if path.find(r'<UDIM>')!=-1 or path.find(r'<udim>')!=-1:
            path=re.sub(r'<UDIM>','????',path)
            path=re.sub(r'<udim>','????',path)
            try:
                report.append('Found \<udim\> expression\n')
            except:
                pass
        if path.find(r'#')!=-1:    
            path=re.sub(r'#.+','',path)
            try:
                report.append('Found FBX path with # expression\n')
            except:
                pass

        detect=re.findall(r'[\^\*\+\{\}\[\]\|"\'~%&<>`]',path)
        if len(detect)>0:
            print ('Special symbols detected (maybe unsupported expression) in file path \"'+ parm.path()) +'\" suspicious symbol \"'+''.join(detect)+'\" .IF THE FILE IS NOT PROCESSED you can debug from here. You can e-mail to gammany@gmail.com to support more expressions.\n'
            try:
                report.append('Special symbols detected (maybe unsupported expression) in file path \"'+ parm.path()) +'\" suspicious symbol \"'+''.join(detect)+'\" .IF THE FILE IS NOT PROCESSED you can debug from here. You can e-mail to gammany@gmail.com to support more expressions.\n'         
                ecount+=1
            except:
                pass
        return path  

    def tryToFixAbsolute(self,parm):
        raw=parm.unexpandedString()
        if raw.find('$HIP')!=0:
            inpth=os.path.dirname(os.path.normpath(os.path.normcase(hou.hipFile.path())))
            parpath=os.path.normpath(os.path.normcase(parm.eval()))
            if parpath.find(inpth)==0:
                pth=parpath.replace(inpth,'$HIP')
                parm.set(pth)
                print ('FIXED Absolute path on node '+parm.path()+' to - \"'+pth+'\"')
                report.append('FIXED Absolute path on node '+parm.path()+' to - \"'+pth+'\"\n')

    def correctAbsolute(self,parm):
        raw=parm.unexpandedString()
        if raw.find('$HIP')!=0:
            if self.chFile.isChecked():
                parpath=os.path.normpath(os.path.normcase(parm.eval()))
                pth=parpath.replace(self.ln_file.text(),'$HIP')
                parm.set(pth)

    def findFiles(self,parm,path):
        global lst
        global report
        files=[]
        path=os.path.normcase(path)
        pth=self.correctWrongExpr(parm)
        fil = os.path.basename(pth)
        if parm.isTimeDependent():
            filePattern=re.sub(r'\d','?',fil)
        else:
            filePattern=fil

        if self.ch_search.isChecked():
            files=[]
            path=self.ln_search.text()
            if os.path.exists(path):
                for d,t,fls in os.walk(path):
                    ch_search='\\'.join([str(d), filePattern])
                    files.extend(glob.glob(ch_search))
            else:
                lst.append('Search path doesn`t exist!!! '+path+' \n')
                report.append('Search path doesn`t exist!!! '+path+' \n')
                ecount+=1
        else:
            ch_search='\\'.join([path, filePattern])
            files=glob.glob(ch_search)
        return files 

    def copyFiles(self,params,arg_path):
        global lst
        global report
        global fcount
        global pcount
        global ecount

        if len(params)>0:
            for p in params:
                try:
                    pcount+=1
                    oldpath=p.unexpandedString()
                    report.append('\n'+str(pcount)+' - param - '+p.path()+' processing \n')
                    files=self.findFiles(p, os.path.dirname(p.eval()))
                    if len(files)>0: 
                        report.append(str(len(files))+' files found for this param \n')
                        for file in files:
                            newPath = '\\'.join([arg_path,os.path.basename(file)])
                            arch.append(newPath)
                            if not os.path.exists(newPath):
                                shutil.copy2(file, newPath)
                                fcount+=1
                                print newPath+' collected'
                                lst.append(os.path.basename(file)+' collected \n')
                                report.append('Old path - '+file+' - New path - '+newPath+'\n')        
                            else:
                                print (file+' already exist')
                                report.append(file+' already exist\n')
                                if self.chupd.isChecked():
                                    if os.path.getsize(newPath)!=os.path.getsize(file):
                                        os.remove(newPath)
                                        shutil.copy2(file, newPath)
                                        fcount+=1
                                        print newPath+' collected'
                                        lst.append(os.path.basename(file)+' collected and overwrited \n')
                                        report.append('Old path - '+file+' - New path (overwrited) - '+newPath+'\n')

                        oldExpr=re.split(r'[/\\]',p.unexpandedString())
                        oldExpr.reverse()
                        newParam='/'.join([self.convToHip(arg_path) , oldExpr[0]])
                        p.set(newParam)
                        report.append('Old parm- '+oldpath+' New parm- '+newParam+'\n')
                    else:
                        erstr='File '+p.unexpandedString()+' on node '+p.node().name()+' in parameter '+p.path()+' NOT FOUND \n'
                        print (erstr)
                        report.append(erstr+'\n')
                        ecount+=1
                except BaseException as e:
                    erstr='ERROR on node '+p.node().name()+'\n'
                    erstr+=str(e)
                    print (erstr)
                    report.append(erstr+'\n')
                    ecount+=1

    def setFilePath(self):
        ospath = QtGui.QFileDialog.getExistingDirectory(self, "Select Path to Save", os.path.dirname(hou.hipFile.path()))
        ospath=os.path.normpath(os.path.normcase(ospath))
        self.ln_file.setText(ospath)
        self.ln_geo.setText(ospath+'\\geometry')
        self.ln_img.setText(ospath+'\\textures')
        self.ln_dop.setText(ospath+'\\dop')
        self.ln_customPath.setText(ospath+'\\other')
    def setFilePath1(self):
        ospath = QtGui.QFileDialog.getExistingDirectory(self, "Select Path to Save", os.path.dirname(hou.hipFile.path()))
        ospath=os.path.normpath(os.path.normcase(ospath))
    def setFilePath2(self):
        ospath = QtGui.QFileDialog.getExistingDirectory(self, "Select Path to Save", os.path.dirname(hou.hipFile.path()))
        ospath=os.path.normpath(os.path.normcase(ospath))
        self.ln_img.setText(ospath)
    def setFilePath3(self):
        ospath = QtGui.QFileDialog.getExistingDirectory(self, "Select Path to Save", os.path.dirname(hou.hipFile.path()))
        ospath=os.path.normpath(os.path.normcase(ospath))
        self.ln_dop.setText(ospath)
    def setFilePath4(self):
        ospath = QtGui.QFileDialog.getExistingDirectory(self, "Select Path to Save", os.path.dirname(hou.hipFile.path()))
        ospath=os.path.normpath(os.path.normcase(ospath))
        self.ln_customPath.setText(ospath)
    def setFilePath6(self):
        ospath = QtGui.QFileDialog.getExistingDirectory(self, "Select Path to Save", os.path.dirname(hou.hipFile.path()))
        ospath=os.path.normpath(os.path.normcase(ospath))
        self.ln_search.setText(ospath)
    
    def copyProcessGeo(self,arg_path):
        if not os.path.exists(arg_path):
            os.makedirs(arg_path)
            report.append('created directory: '+arg_path+'\n')
        if arg_path:
            nodes=self.collectNodesByType('geo')
            params=self.collectParams(nodes)
            self.copyFiles(params,arg_path)

    def copyProcessTextures(self,arg_path):
        if not os.path.exists(arg_path):
            os.makedirs(arg_path)
            report.append('created directory: '+arg_path+'\n')
        if arg_path:
            nodes=self.collectNodesByType('img')
            params=self.collectParams(nodes)
            self.copyFiles(params,arg_path)

    def copyProcessDops(self,arg_path):
        if not os.path.exists(arg_path):
            os.makedirs(arg_path)
            report.append('created directory: '+arg_path+'\n')
        if arg_path:
            nodes=self.collectNodesByType('dop')
            params=self.collectParams(nodes)
            self.copyFiles(params,arg_path)

    def copyProcessOther(self, arg_parm_name, arg_path):
        if not os.path.exists(arg_path):
            os.makedirs(arg_path)
        global lst
        global report
        lst=['Collected items: \n \n']
        filteredParms=[]
        if arg_path:
            nodes=self.collectNodesByType('')
            for n in nodes:
                for par in n.parms():
                    if par.name()==arg_parm_name:
                        if self.checkExceptions(par)==1:
                            filteredParms.append(par)
            if len(filteredParms)>0:        
                self.copyFiles(filteredParms,arg_path)

    def copyProcessHip(self, arg_path):

        if not os.path.exists(arg_path):
            os.makedirs(arg_path)
        filenm=arg_path.replace('\\','\\\\')
        filenm+='\\'+hou.hipFile.basename()[:-4]+'_collected.hip'
        filenm=os.path.normpath(os.path.normcase(filenm))
        filenm=hou.expandString(filenm).replace('\\','/')
        hou.hipFile.save(filenm,True)
        print ('FILE SAVED in '+ filenm )

        report.append('----------\n')
        report.append('FILE SAVED in '+ filenm +' \n')

        hou.ui.displayMessage('Collected File will be loaded...')
        hou.hipFile.clear(True)
        hou.hipFile.load(filenm, False, False)

    
    def archiveCollect(self):
        pth=hou.hipFile.path()[:-4]
        zf = zipfile.ZipFile(pth +'.zip', mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64 = True)
        arch.append(hou.hipFile.path())
        for f in arch:
            zf.write(f)
        zf.close()
        print 'ARCHIVE CREATED '+pth +'.zip'

        report.append('----------\n')
        report.append('ARCHIVE CREATED '+pth +'.zip'+'\n') 
    
    def generateReport(self):
        file = open(self.ln_file.text()+'\\report.txt', 'w')
        file.write(''.join(report))
        file.close()
        print ('Report generated '+self.ln_file.text()+'\\report.txt')

    def collectFiles(self):
        global lst
        global report
        global fcount
        global pcount
        global ecount
        global arch
        arch = []
        ecount=0
        fcount=0
        pcount=0
        lst=[]
        report=[]

        self.btn_collect.setText('WAIT...')
        print '\n' * 100
        lst=['Collected: \n \n']

        report=[datetime.datetime.now().strftime("%c")+'\n ']

        if hou.hipFile.hasUnsavedChanges():
            if hou.ui.displayConfirmation('The file has unsaved changes. SAVE?'):
                pass
            else:
                hou.ui.displayMessage('Canceled') 
                return -1
        if self.chGeo.isChecked():
            report.append('Processing geometry:\n')
            self.copyProcessGeo(self.ln_geo.text())
        if self.chImg.isChecked():
            report.append('Processing textures:\n')
            self.copyProcessTextures(self.ln_img.text())
        if self.chDop.isChecked():
            report.append('Processing DOPs:\n')
            self.copyProcessDops(self.ln_dop.text())
        if self.chCustom.isChecked():
            report.append('Processing custom:\n')
            self.copyProcessOther(self.ln_attr.text(), self.ln_customPath.text())

        if self.chFile.isChecked():
            self.copyProcessHip(self.ln_file.text())
        else:
            hou.hipFile.save()
            print 'FILE SAVED'

            report.append('----------\n')
            report.append('FILE SAVED\n') 
            
        if self.charch.isChecked():
                self.archiveCollect()

        report.insert(1,('---\n'+str(pcount)+' parameters processed\n'+str(fcount)+' - Files copied\n'+str(ecount)+' - Errors\n---\n'))
        self.generateReport()

        if len(lst)>1:
            lst.insert(0,('---\n'+str(pcount)+' parameters processed\n'+str(fcount)+' - Files copied\n'+str(ecount)+' - Errors\n---\n'))
            hou.ui.displayMessage(''.join(lst))
        else:
            hou.ui.displayMessage('All files already collected')
        self.btn_collect.setText('Collect')

    def checkLinks(self):
        global lst
        global report
        global fcount
        global pcount
        global ecount
        arch = []
        ecount=0
        fcount=0
        pcount=0
        lst=[]
        report=[]

        self.ch_search.setChecked(0)
        lst=['These path are not collected: \n \n']
        nodes=self.collectNodesByType('')
        params=self.collectParams(nodes)
        ae=0
        an=0
        rn=0
        ok=0
        if len(params)>0:
            for p in params: 
                self.tryToFixAbsolute(p)
                pthOS=p.eval()
                pthHIP=p.unexpandedString()
                files=self.findFiles(p, os.path.dirname(pthOS))
                if len(files)>0 :
                    if (pthHIP.find('$HIP')!=0 and pthHIP.find('$JOB')!=0):
                        ae+=1
                        lst.append(pthHIP +'    in node    '+p.node().path()+' has absolute path but exist\n') 
                    else:
                        ok+=1
                else:
                    if (pthHIP.find('$HIP')!=0 and pthHIP.find('$JOB')!=0):
                        an+=1
                        lst.append(pthOS +'    in node    '+p.node().path()+' has absolute path and NOT exist\n')
                    else:
                        rn+=1
                        lst.append(pthOS +'    in node    '+p.node().path()+' has relative path and NOT exist\n')
            if len(lst)>1:
                strerr=''
                if ok>0:
                    strerr+=str(ok)+' files are OK\n'
                if ae>0:
                    strerr+=str(ae)+' files has absolute path but exist (watch console)\n'
                if an>0:
                    strerr+=str(an)+' files has absolute path and NOT exist (watch console)\n'
                if rn>0:
                    strerr+=str(rn)+' files has relative path and NOT exist (watch console)\n' 
                hou.ui.displayMessage(strerr)
                print (''.join(lst))
            else:
                hou.ui.displayMessage('All files already collected.')