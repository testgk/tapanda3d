import jenkins.model.*
import hudson.security.*

def instance = Jenkins.getInstance()
def adminPassword = System.getenv( 'JENKINS_ADMIN_PASSWORD' ) ?: 'changeme'

def hudsonRealm = new HudsonPrivateSecurityRealm( false )
hudsonRealm.createAccount( 'admin', adminPassword )
instance.setSecurityRealm( hudsonRealm )

def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead( false )
instance.setAuthorizationStrategy( strategy )
instance.save()

println 'Jenkins initialized with admin user. Use JENKINS_API_TOKEN from keys.env for API calls.'
