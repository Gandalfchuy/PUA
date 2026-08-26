import { describe, it, expect, beforeEach } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ɵresolveComponentResources as resolveComponentResources } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { ProcesoReeducacionComponent } from './proceso-reeducacion';

describe('ProcesoReeducacionComponent', () => {
  let component: ProcesoReeducacionComponent;
  let fixture: ComponentFixture<ProcesoReeducacionComponent>;

  beforeEach(async () => {
    await resolveComponentResources(() => Promise.resolve('<div></div>'));
    await TestBed.configureTestingModule({
      imports: [ProcesoReeducacionComponent],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ProcesoReeducacionComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
