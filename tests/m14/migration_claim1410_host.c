#include <assert.h>
#include <engine/winmigration1410.h>

int main(void){
 const uint8_t installed[]={1,2,3,4},prior[]={5,6,7,8},changed[]={1,2,3,5};
 assert(win_migration_postimage1410(4,installed,4,4,installed,4,0,0,0,0));
 assert(win_migration_postimage1410(4,installed,4,4,installed,4,1,4,prior,4));
 assert(!win_migration_postimage1410(4,installed,4,4,installed,4,1,4,installed,4));
 assert(!win_migration_postimage1410(4,changed,4,4,installed,4,1,4,prior,4));
 assert(!win_migration_postimage1410(3,installed,4,4,installed,4,0,0,0,0));

 win_tx_reg147 claim={.root=2,.view=32};
 assert(win_migration_same_value1410(2,32,"Software\\Example","Name",&claim,"software\\example","NAME"));
 assert(!win_migration_same_value1410(2,64,"Software\\Example","Name",&claim,"software\\example","NAME"));
 assert(!win_migration_same_value1410(1,32,"Software\\Example","Name",&claim,"software\\example","NAME"));
 claim.root=1;
 assert(win_migration_same_value1410(1,64,"Software\\Example","Name",&claim,"software\\example","NAME"));
 assert(!win_migration_same_value1410(1,64,"Software\\Example","Other",&claim,"software\\example","NAME"));
 return 0;
}
