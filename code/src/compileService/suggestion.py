import commands

def suggestJava(path, filename, username):
    x = ""
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/android.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/basic.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/braces.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/clone.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/codesize.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/comments.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/controversial.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/coupling.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/design.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/empty.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/finalizers.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/imports.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/j2ee.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/javabeans.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/junit.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/logging-jakarta-commons.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/logging-java.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/metrics.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/migrating.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/migrating_to_13.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/migrating_to_14.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/migrating_to_15.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/migrating_to_junit4.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/naming.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/optimizations.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/strictexception.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/strings.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/sunsecure.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/typeresolution.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/unnecessary.xml')
    x += "\n"
    x += commands.getoutput('/home/'+username+'/pmd-bin-5.8.1/bin/run.sh pmd -d '+path+'/'+filename+'.java -f text -R rulesets/java/unusedcode.xml')
    x += "\n"

    return x
