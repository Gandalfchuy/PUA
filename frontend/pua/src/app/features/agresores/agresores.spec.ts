import { describe, it, expect, beforeEach } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ɵresolveComponentResources as resolveComponentResources } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter } from '@angular/router';
import { AgresoresComponent } from './agresores';

describe('AgresoresComponent', () => {
  let component: AgresoresComponent;
  let fixture: ComponentFixture<AgresoresComponent>;

  beforeEach(async () => {
    await resolveComponentResources(() => Promise.resolve('<div></div>'));
    await TestBed.configureTestingModule({
      imports: [AgresoresComponent],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([])
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AgresoresComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
