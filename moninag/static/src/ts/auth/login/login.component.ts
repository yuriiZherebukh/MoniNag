import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { AlertService, AuthenticationService } from '../_services/index';


@Component({
    selector: 'login',
    template: require('./login.component.html')
})

export class LoginComponent {
    model: any = {};
    loading = false;

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private alertService: AlertService) { }

    login() {
        this.loading = true;
        this.authenticationService.login(this.model.email, this.model.password)
            .subscribe(
                data => {
                    if(data.success) {
                        window.location.href = data.message;
                    } else {
                        this.alertService.error(data.error);
                        this.loading = false;
                    }
                },
                error => {
                    this.alertService.error(error._body);
                    this.loading = false;
                }
            );
    }
}
