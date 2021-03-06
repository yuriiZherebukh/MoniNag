import { Component, OnInit, Input, ViewEncapsulation } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { DialogPreset, DialogPresetBuilder, Modal, VexModalModule } from 'angular2-modal/plugins/vex';
import { MdDialog, MdDialogRef } from '@angular/material';

import { Location } from '@angular/common';
import 'rxjs/add/operator/switchMap';

import { overlayConfigFactory } from "angular2-modal";

import { Check } from './check';
import { ChecksService } from './checks.service';
import { CheckUpdateComponent } from './check-update.component';
import { CheckDeleteComponent } from './check-delete.component';
import { ChecksDialog } from './checks-activate-deactivate.component';


@Component({
    selector: 'checkdetail-app',
    template: require('./check-detail.component.html'),
    providers: [ChecksService],
    styles: [ require('./checks.less').toString() ],
    encapsulation: ViewEncapsulation.None
})


export class CheckDetailComponent implements OnInit {

    constructor(
        private checksService: ChecksService,
        private route: ActivatedRoute,
        private location: Location,
        public modal: Modal,
        public dialog: MdDialog,
    ) { }

    check: Check;
    selectedCheck: Check;

    ngOnInit(): void {
        this.route.params
            .switchMap((params: Params) => this.checksService.getCheck(+params['id']))
            .subscribe(check => { this.check = check['response']});
    }

    openDialog($event:any) {
        let dialogRef = this.dialog.open(ChecksDialog);
        dialogRef.componentInstance.checkState = this.check.state;
        dialogRef.componentInstance.actionName = this.check.state ? 'deactivate' : 'activate';
        dialogRef.afterClosed().subscribe(result => {
            if (result === undefined) return;
            result ? this.activate() : this.deactivate();
        });
    }


    onSelect(check: Check): void {
        this.selectedCheck = check;
    }

    deleteModal() {
        return new DialogPresetBuilder<DialogPreset>(this.modal)
            .content(CheckDeleteComponent)
            .isBlocking(false)
            .open();
    }

    deactivate(): void {
        this.checksService.deactivate(this.check)
            .subscribe(() => this.goBack());
    }

    activate(): void {
        this.checksService.activate(this.check)
            .subscribe(() => this.goBack());
    }

    goBack(): void {
        this.location.back();
    }

    renderModal() {
        return new DialogPresetBuilder<DialogPreset>(this.modal)
            .content(CheckUpdateComponent)
            .isBlocking(false)
            .open();
    }
}
