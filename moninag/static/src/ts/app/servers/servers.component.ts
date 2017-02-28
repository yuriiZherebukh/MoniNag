import { Component, OnInit, OnChanges } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';

import { Server, states } from './model';
import { ServersService } from './service';
import { ServersEditComponent } from './edit-server.component'
import { ServerComponent } from './server.component'

@Component({
    selector: 'servers-app',
    template: require('./servers.component.html'),
    providers: [ServersService]
})

export class ServersComponent implements OnInit {

    servers: Server[];
    selectedServer: Server;
    deletedServer: Server;
    server: Server;

    constructor(
        private serversService: ServersService,
        private router: Router) { }

    ngOnInit() {
        this.serversService.getServers()
            .subscribe(servers => {
                this.servers = servers['response']
            })
    }

    onSelect(server: Server): void {
        this.selectedServer = server;
    }

    gotoEdit(): void {
        this.router.navigate(['server', this.selectedServer.id]);
    }
    handleServerAdded(server: Server) {
        this.servers.push(server)
    }
    add() {
        this.router.navigate(['server-add']);
    }
}