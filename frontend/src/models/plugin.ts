export default class Plugin {
    name: string = '';      
    script: string = '';      
    website: string = '';
    checkInterval: number = 0;
    state: boolean = false;
    active: boolean = false;
    lastChecked?: string; 
}